"""Self-check for ffmpeg-mcp server. Run: python3 test_server.py

Generates a short test clip, exercises every tool, asserts expected outputs.
Requires ffmpeg + ffprobe on PATH. No pytest — plain asserts per repo rules.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import server  # noqa: E402

TMP = Path(tempfile.mkdtemp(prefix="ffmcp_selftest_"))
os.environ["FFMPEG_MCP_WORKDIR"] = str(TMP)
server.DEFAULT_DIR = str(TMP)  # rebind module-level workdir
tm = server.mcp._tool_manager._tools


def call(name: str, *a, **kw):
    return tm[name].fn(*a, **kw)


def make_clip() -> Path:
    src = TMP / "input.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-f", "lavfi", "-i", "testsrc2=duration=3:size=640x360:rate=30",
         "-f", "lavfi", "-i", "sine=frequency=440:duration=3",
         "-c:v", "libx264", "-c:a", "aac", "-shortest", str(src)],
        check=True, capture_output=True,
    )
    return src


def expect_file(p: Path, min_size: int = 1000) -> None:
    assert p.exists(), f"missing output {p}"
    assert p.stat().st_size >= min_size, f"output too small: {p}"


def main() -> int:
    src = make_clip()
    assert src.exists() and src.stat().st_size > 1000

    # 12 tools registered
    expected = {
        "probe", "transcode", "cut", "extract_audio", "thumbnail", "make_gif",
        "concat", "normalize_audio", "compress", "extract_frames",
        "add_subtitles", "strip_metadata",
    }
    assert set(tm) == expected, f"tool set mismatch: {set(tm) ^ expected}"

    # probe → valid JSON
    meta = json.loads(call("probe", str(src)))
    assert meta["streams"], "probe returned no streams"
    assert meta["streams"][0]["width"] == 640

    # editing
    call("cut", str(src), start="0", duration="1")
    expect_file(TMP / "input_cut.mp4")
    call("transcode", str(src), width=320, height=180)
    expect_file(TMP / "input_transcoded.mp4")
    call("concat", [str(src), str(src)], output="joined.mp4")
    expect_file(TMP / "joined.mp4")

    # picture
    call("thumbnail", str(src), time="00:00:01")
    expect_file(TMP / "input.jpg", 500)
    call("make_gif", str(src), duration="2")
    expect_file(TMP / "input.gif")
    call("extract_frames", str(src), fps=2)
    frames_dir = TMP / "input_frames"
    assert frames_dir.is_dir() and len(list(frames_dir.iterdir())) >= 1

    # audio
    call("extract_audio", str(src))
    expect_file(TMP / "input.m4a")
    call("normalize_audio", str(src))
    expect_file(TMP / "input_loudnorm.mp4")
    call("compress", str(src), quality="low")
    expect_file(TMP / "input_transcoded.mp4")
    call("strip_metadata", str(src))
    expect_file(TMP / "input_clean.mp4")

    # subtitles
    srt = TMP / "sub.srt"
    srt.write_text("1\n00:00:00,000 --> 00:00:02,000\nhello test\n")
    call("add_subtitles", str(src), str(srt))
    expect_file(TMP / "input_subbed.mp4")

    # error paths
    bad_calls = [
        lambda: call("probe", "nope.mp4"),
        lambda: call("cut", str(src), start="0"),        # no duration/end
        lambda: call("compress", str(src), quality="bogus"),
        lambda: call("concat", [str(src)]),              # only 1 input
    ]
    for fn in bad_calls:
        try:
            fn()
            raise AssertionError(f"expected FFmpegError from {fn}")
        except server.FFmpegError:
            pass

    print(f"OK — 12 tools registered, all exercised, error paths caught. tmp={TMP}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
