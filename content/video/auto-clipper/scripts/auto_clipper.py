#!/usr/bin/env python3
"""Auto Clipper — extract engaging short clips from a long video.

Detects scene cuts (ffmpeg `select=gt(scene,T)`) and audio-energy peaks
(per-frame RMS via ffmpeg astats), scores candidate windows, then cuts
5–15 s clips with fades. Deterministic, stdlib + ffmpeg only.

ponytail: scoring is energy+cut density; upgrade path = add speech/transcript
  weighting (whisper) when clips must follow spoken highlights.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def probe_duration(src: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", src],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def detect_scenes(src: str, threshold: float) -> list[float]:
    """Return timestamps of visual scene changes."""
    p = subprocess.run(
        ["ffmpeg", "-i", src, "-vf", f"select='gt(scene,{threshold})',showinfo",
         "-f", "null", "-"],
        capture_output=True, text=True)
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", p.stderr)]


def audio_energy(src: str, win: float = 0.5) -> list[tuple[float, float]]:
    """Per-window RMS loudness via volumedetect-style frames.

    Uses `astats` with metadata per window; returns [(t_start, rms_db)].
    """
    p = subprocess.run(
        ["ffmpeg", "-i", src, "-af",
         f"aformat=channel_layouts=mono,asetnsamples=n={int(win * 44100)},"
         "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level",
         "-f", "null", "-"],
        capture_output=True, text=True)
    pts, vals = re.findall(r"pts_time:([0-9.-]+)", p.stderr), \
               re.findall(r"RMS_level=(-?[0-9.inf]+)", p.stderr)
    res = []
    for t, v in zip(pts, vals):
        try:
            res.append((float(t), float(v)))
        except ValueError:
            continue
    return res


def score_windows(dur: float, scenes: list[float], energy: list[tuple[float, float]],
                  lo: int, hi: int, step: float = 1.0) -> list[dict]:
    """Slide a window over the timeline; score = cut density + normalized RMS."""
    if not energy:
        raise SystemExit("no audio energy data — does the input have an audio stream?")
    rms_vals = [e[1] for e in energy]
    floor = min(rms_vals)          # dB, quieter bound
    ceil_ = max(rms_vals)
    span = max(ceil_ - floor, 1e-6)

    def norm_rms(t0: float, t1: float) -> float:
        sel = [v for t, v in energy if t0 <= t < t1]
        if not sel:
            return 0.0
        avg = sum(sel) / len(sel)
        return (avg - floor) / span

    scored = []
    start = 0.0
    while start + lo <= dur:
        best = None
        for length in range(lo, hi + 1):
            if start + length > dur:
                break
            t0, t1 = round(start, 2), round(start + length, 2)
            cuts = sum(1 for s in scenes if t0 <= s <= t1)
            score = 0.6 * norm_rms(t0, t1) + 0.4 * min(cuts / max(1, length / 3), 1.0)
            if best is None or score > best["score"]:
                best = dict(start=t0, end=t1, duration=length, cuts=cuts,
                            score=round(score, 4))
        if best:
            scored.append(best)
        start += step
    return sorted(scored, key=lambda c: -c["score"])


def dedupe(clips: list[dict], max_n: int, overlap: float = 0.5,
           spread_bonus: float = 0.15, dur: float = 0.0) -> list[dict]:
    """Keep top-N clips, dropping ones overlapping >overlap fraction of shorter clip.

    spread_bonus: score boost per clip already kept far (>25% of timeline) from
    the candidate — distributes picks across the video instead of clustering.
    """
    kept: list[dict] = []

    def boost(c: dict) -> float:
        if not dur or not kept:
            return 0.0
        far = sum(1 for k in kept
                  if abs(c["start"] - k["start"]) > 0.25 * dur)
        return far * spread_bonus

    kept: list[dict] = []
    pool = list(clips)
    while pool and len(kept) < max_n:
        # re-score each round so the spread bonus sees what's already kept
        pool.sort(key=lambda c: -(c["score"] + boost(c)))
        c = pool.pop(0)
        clash = any(
            min(c["end"], k["end"]) - max(c["start"], k["start"])
            > overlap * min(c["duration"], k["duration"]) for k in kept)
        if not clash:
            kept.append(c)
    return sorted(kept, key=lambda c: c["start"])


def cut(src: str, out: Path, start: float, length: float, fade_in: float,
        fade_out: float, crf: int) -> None:
    vf = ""
    af_parts = []
    if fade_in > 0:
        af_parts.append(f"afade=t=in:st=0:d={fade_in}")
    if fade_out > 0:
        af_parts.append(f"afade=t=out:st={max(0, length - fade_out):.2f}:d={fade_out}")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start:.3f}",
           "-i", src, "-t", f"{length:.3f}"]
    if af_parts:
        cmd += ["-af", ",".join(af_parts)]
    cmd += ["-c:v", "libx264", "-crf", str(crf), "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k", str(out)]
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default="clips/")
    ap.add_argument("--min-duration", type=int, default=5)
    ap.add_argument("--max-duration", type=int, default=15)
    ap.add_argument("--scene-threshold", type=float, default=0.3)
    ap.add_argument("--audio-threshold", type=float, default=0.7)
    ap.add_argument("--max-clips", type=int, default=8)
    ap.add_argument("--fade-in", type=float, default=0.5)
    ap.add_argument("--fade-out", type=float, default=0.5)
    ap.add_argument("--quality", type=int, default=20)
    args = ap.parse_args()

    src = args.input
    outdir = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)

    dur = probe_duration(src)
    print(f"[auto-clipper] {src}: {dur:.1f}s", file=sys.stderr)
    scenes = detect_scenes(src, args.scene_threshold)
    print(f"[auto-clipper] {len(scenes)} scene cuts detected", file=sys.stderr)
    energy = audio_energy(src)
    print(f"[auto-clipper] {len(energy)} audio windows analyzed", file=sys.stderr)

    candidates = score_windows(dur, scenes, energy, args.min_duration,
                               args.max_duration)
    clips = dedupe(candidates, args.max_clips, dur=dur)

    manifest = []
    for i, c in enumerate(clips, 1):
        name = outdir / f"clip_{i:02d}.mp4"
        cut(src, name, c["start"], c["duration"], args.fade_in, args.fade_out, args.quality)
        d = probe_duration(str(name))
        rec = dict(file=str(name), **c, actual_duration=round(d, 2))
        manifest.append(rec)
        print(f"[auto-clipper] {name}  {c['start']}-{c['end']}s  score={c['score']}  cuts={c['cuts']}")

    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"[auto-clipper] wrote {len(manifest)} clips + manifest.json")


if __name__ == "__main__":
    main()
