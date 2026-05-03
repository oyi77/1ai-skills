#!/usr/bin/env python3
"""
AI 视频脚本生成器 — 根据主题生成完整视频脚本。
包含：标题、分镜表、画面提示词、配音文案。

Usage:
    python generate_script.py --topic "智能水杯产品介绍" --duration 30
    python generate_script.py --topic "Why humans dream" --duration 60 --style educational
    python generate_script.py --topic "..." --output json
    python generate_script.py --topic "..." --output markdown
"""

import argparse
import json
import math
import os
import subprocess
import sys
from datetime import datetime

STYLE_MAP = {
    "commercial": {"cn": "商业", "desc": "专业、权威、产品导向"},
    "story": {"cn": "故事", "desc": "情感、冲突、转折"},
    "educational": {"cn": "教育/科普", "desc": "清晰、逻辑、知识点"},
    "entertainment": {"cn": "娱乐", "desc": "轻松、有趣、网感"},
}

PLATFORM_DURATIONS = {
    "douyin": (15, 60),
    "bilibili": (180, 600),
    "youtube": (180, 600),
    "weixin": (30, 180),
}


def call_omniroute(prompt, system_prompt=None):
    """Call OmniRoute for generation."""
    omniroute = os.path.expanduser("~/.openclaw/workspace/scripts/omniroute")
    if not os.path.exists(omniroute):
        omniroute = "omniroute"

    cmd = [omniroute, "--prompt", prompt]
    if system_prompt:
        cmd.extend(["--system", system_prompt])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def generate_video_script(topic, duration, style, use_llm=True):
    """Generate a complete video script with scenes, prompts, and narration."""
    style_info = STYLE_MAP.get(style, STYLE_MAP["educational"])

    # Calculate scene count based on duration
    if duration <= 15:
        num_scenes = 3
    elif duration <= 30:
        num_scenes = 4
    elif duration <= 60:
        num_scenes = 6
    else:
        num_scenes = max(6, duration // 15)

    # Try LLM generation
    if use_llm:
        llm_prompt = (
            f"生成一个 {duration} 秒的视频脚本。\n"
            f"主题: {topic}\n"
            f"风格: {style_info['cn']} ({style_info['desc']})\n"
            f"场次数: {num_scenes}\n\n"
            f"请输出 JSON 格式，结构如下:\n"
            f'{{"title": "视频标题", "duration_sec": {duration}, '
            f'"style": "{style_info["cn"]}", '
            f'"target_audience": "目标受众", '
            f'"scenes": ['
            f'{{"id": 1, "time_range": "0-5s", "duration_sec": 5, '
            f'"visual": "画面描述", "camera": "镜头运动", '
            f'"prompt_cn": "中文AI画面提示词", '
            f'"prompt_en": "English AI image/video prompt", '
            f'"narration": "配音文案", '
            f'"subtitle": "字幕文字"}}], '
            f'"full_narration": "完整配音稿"}}'
        )

        system = (
            "你是专业视频脚本编剧。生成的脚本要实用、可执行，提示词要适配 "
            "CogVideoX/Midjourney/SD 等主流 AI 工具。输出纯 JSON。"
        )

        llm_result = call_omniroute(llm_prompt, system)
        if llm_result:
            try:
                start = llm_result.find("{")
                end = llm_result.rfind("}") + 1
                if start >= 0 and end > start:
                    return json.loads(llm_result[start:end])
            except (json.JSONDecodeError, ValueError):
                pass

    # Fallback: template generation
    scene_dur = duration / num_scenes
    scenes = []

    for i in range(num_scenes):
        t_start = round(i * scene_dur)
        t_end = round((i + 1) * scene_dur)

        scene = {
            "id": i + 1,
            "time_range": f"{t_start}-{t_end}s",
            "duration_sec": t_end - t_start,
        }

        if i == 0:
            scene["visual"] = f"[开篇画面 — 吸引注意力，与{topic}相关]"
            scene["camera"] = "[推进/特写]"
            scene["prompt_cn"] = f"[{topic}相关的开场画面，高质量，电影感]"
            scene["prompt_en"] = f"[Opening shot related to {topic}, cinematic, high quality --ar 16:9]"
            scene["narration"] = f"[开篇 hook — 引起观众兴趣]"
            scene["subtitle"] = f"[{topic}]"
        elif i == num_scenes - 1:
            scene["visual"] = "[结尾画面 — 品牌/CTA]"
            scene["camera"] = "[拉远/定格]"
            scene["prompt_cn"] = "[结尾画面，温暖/专业氛围]"
            scene["prompt_en"] = "[Closing shot, warm lighting, professional --ar 16:9]"
            scene["narration"] = "[行动号召 — 关注/点赞/链接]"
            scene["subtitle"] = "[关注我 / 了解更多]"
        else:
            scene["visual"] = f"[核心内容画面 {i}]"
            scene["camera"] = "[中景/切换]"
            scene["prompt_cn"] = f"[第{i}个要点的视觉化画面]"
            scene["prompt_en"] = f"[Visual for point {i}, detailed, --ar 16:9]"
            scene["narration"] = f"[要点 {i} 的配音文案]"
            scene["subtitle"] = f"[要点 {i} 关键词]"

        scenes.append(scene)

    return {
        "title": f"[{topic}]",
        "duration_sec": duration,
        "style": style_info["cn"],
        "target_audience": "[填写目标受众]",
        "scenes": scenes,
        "full_narration": "[完整配音稿 — 根据各场次配音拼接]",
        "note": "模板已生成 — 请填写方括号内容，或配置 OmniRoute 后重新运行以获得完整脚本"
    }


def format_markdown(script):
    """Format script as readable markdown."""
    lines = []
    lines.append(f"# {script.get('title', 'Video Script')}\n")
    lines.append(f"- **时长**: {script.get('duration_sec', '?')}秒")
    lines.append(f"- **风格**: {script.get('style', 'N/A')}")
    lines.append(f"- **受众**: {script.get('target_audience', 'N/A')}\n")

    lines.append("## 分镜表\n")
    for scene in script.get("scenes", []):
        lines.append(f"### 场次{scene['id']}（{scene.get('time_range', '?')}）")
        lines.append(f"- **画面**: {scene.get('visual', '')}")
        lines.append(f"- **镜头**: {scene.get('camera', '')}")
        lines.append(f"- **提示词(中)**: {scene.get('prompt_cn', '')}")
        lines.append(f"- **提示词(英)**: {scene.get('prompt_en', '')}")
        lines.append(f"- **配音**: {scene.get('narration', '')}")
        lines.append(f"- **字幕**: {scene.get('subtitle', '')}")
        lines.append("")

    lines.append("## 完整提示词列表\n")
    for scene in script.get("scenes", []):
        lines.append(f"{scene['id']}. {scene.get('prompt_en', '')}")
    lines.append("")

    lines.append("## 完整配音稿\n")
    lines.append(script.get("full_narration", "[见各场次配音]"))

    if script.get("note"):
        lines.append(f"\n---\n*{script['note']}*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AI视频脚本生成器")
    parser.add_argument("--topic", required=True, help="视频主题 / Video topic")
    parser.add_argument("--duration", type=int, default=30,
                        help="时长（秒）/ Duration in seconds (default: 30)")
    parser.add_argument("--style", choices=list(STYLE_MAP.keys()),
                        default="educational", help="风格 / Style")
    parser.add_argument("--output", choices=["json", "markdown"], default="markdown",
                        help="输出格式 / Output format")
    parser.add_argument("--no-llm", action="store_true",
                        help="不调用LLM，仅输出模板 / Template only, skip LLM")
    args = parser.parse_args()

    script = generate_video_script(args.topic, args.duration, args.style,
                                    use_llm=not args.no_llm)

    if args.output == "json":
        print(json.dumps(script, ensure_ascii=False, indent=2))
    else:
        print(format_markdown(script))


if __name__ == "__main__":
    main()
