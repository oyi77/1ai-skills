"""
Scene Analyzer — AI vision analysis per scene
Analyzes each keyframe to understand:
- What's being shown
- Mood & visual style
- On-screen text / CTA
- Suggests better version
"""

import os, json, base64, urllib.request, urllib.error
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from prompt_library import STYLES

NVIDIA_KEY = os.environ.get("NVIDIA_API_KEY")
GROQ_KEY = os.environ.get("GROQ_API_KEY")


def analyze_scene(scene: dict, product_category: str = "unknown") -> dict:
    """
    Analyze a single scene keyframe with vision AI.
    Returns analysis dict with content, style, text, upgrade suggestions.
    """
    frame_path = scene["keyframe"]
    if not os.path.exists(frame_path):
        return {"error": "keyframe not found"}

    with open(frame_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    styles_str = ", ".join(STYLES.keys())

    prompt = f"""You are a professional video content strategist analyzing a competitor's video scene.

Analyze this scene image and respond ONLY in JSON:
{{
  "scene_type": "product_only | model_only | product_with_model | text_overlay | transition | cta",
  "has_person": true or false,
  "has_product": true or false,
  "subject": "what is the main focus (product, person, environment)",
  "person_description": "if person visible: gender, style, clothing, expression — else null",
  "product_description": "if product visible: what product, color, size — else null",
  "visual_style": "one of: {styles_str}",
  "mood": "e.g. energetic, calm, luxury, playful, professional",
  "on_screen_text": "any visible text or CTA in the scene, or null",
  "color_palette": "dominant colors e.g. dark charcoal, gold, white",
  "composition": "e.g. center product, rule of thirds, close-up, wide shot",
  "weakness": "what could be improved about this scene",
  "upgrade_prompt": "a detailed hyperrealistic image generation prompt to create a BETTER version. If person present, describe them naturally (no ethnicity). Make it more professional and visually striking.",
  "upgrade_animation": "describe how this scene should be animated for maximum impact"
}}"""

    # Try NVIDIA vision model
    payload = json.dumps(
        {
            "model": "meta/llama-3.2-11b-vision-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"},
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            "max_tokens": 800,
            "temperature": 0.1,
        }
    ).encode()

    headers = {
        "Authorization": f"Bearer {NVIDIA_KEY}",
        "Content-Type": "application/json",
    }

    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            content = data["choices"][0]["message"]["content"].strip()
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
    except Exception as e:
        print(f"    ⚠️ Vision API error: {e}. Using fallback analysis...")
        return _fallback_analysis(scene)


def _fallback_analysis(scene: dict) -> dict:
    """Fallback when vision API fails — return generic upgrade prompts"""
    return {
        "scene_type": "product_shot",
        "subject": "product",
        "visual_style": "dark_moody",
        "mood": "professional",
        "on_screen_text": None,
        "color_palette": "dark, dramatic",
        "composition": "center product",
        "weakness": "Could be more visually striking and professional",
        "upgrade_prompt": (
            "cinematic hyperrealistic product photography, dramatic studio lighting, "
            "dark moody background, ultra detailed, 8K, professional commercial quality, "
            "Sony A7III, shallow depth of field, film grain"
        ),
        "upgrade_animation": "slow dramatic reveal with light sweep, cinematic slow motion",
    }


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe competitor voiceover using Whisper (local) or fallback
    """
    try:
        import whisper

        print("  🎙️ Transcribing audio with Whisper...")
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="id")  # Indonesian
        text = result["text"].strip()
        print(f"  ✅ Transcription: {text[:100]}...")
        return text
    except ImportError:
        print("  ⚠️ Whisper not available, using empty transcript")
        return ""
    except Exception as e:
        print(f"  ⚠️ Transcription error: {e}")
        return ""


def improve_script(
    original_script: str, scenes_analysis: list, product_category: str, groq_key: str
) -> list:
    """
    Rewrite competitor VO script to be more compelling.
    Returns list of VO text per scene.
    """
    n_scenes = len(scenes_analysis)
    scenes_context = "\n".join(
        [
            f"Scene {i+1} ({s.get('duration',5):.1f}s): {a.get('scene_type','product')} — {a.get('subject','product')}"
            for i, (s, a) in enumerate(scenes_analysis)
        ]
    )

    prompt = f"""You are an expert Indonesian copywriter and content strategist.

A competitor has this video content structure:
{scenes_context}

Original competitor script (if available):
"{original_script or 'No transcript available'}"

Product category: {product_category}

Your task: Write a BETTER voiceover script for each scene.
Requirements:
- Bahasa Indonesia yang natural dan conversational
- More emotional, more relatable, more compelling than competitor
- Hook di scene 1 yang langsung menarik perhatian
- Build tension/curiosity in middle scenes
- Strong CTA di scene terakhir
- Setiap VO sesuai dengan durasi scene (pendek = 1-2 kalimat, panjang = 2-3 kalimat)

Respond ONLY in JSON:
{{
  "improved_script": [
    {{"scene": 1, "vo": "voiceover text for scene 1"}},
    {{"scene": 2, "vo": "voiceover text for scene 2"}}
  ],
  "hook_analysis": "why your hook is better than competitor",
  "overall_strategy": "what makes your version more compelling"
}}"""

    payload = json.dumps(
        {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1500,
            "temperature": 0.7,
        }
    ).encode()

    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json",
    }

    try:
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=payload,
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            content = data["choices"][0]["message"]["content"].strip()
            content = content.replace("```json", "").replace("```", "").strip()
            result = json.loads(content)
            return result
    except Exception as e:
        print(f"  ⚠️ Script improvement error: {e}")
        # Fallback: generic VO per scene
        return {
            "improved_script": [
                {
                    "scene": i + 1,
                    "vo": f"Produk terbaik untuk kebutuhan kamu. Scene {i+1}.",
                }
                for i in range(n_scenes)
            ],
            "hook_analysis": "Generic fallback",
            "overall_strategy": "Basic",
        }


if __name__ == "__main__":
    # Test with dummy scene
    test_scene = {
        "id": 1,
        "duration": 5.0,
        "keyframe": "/tmp/test_frame.jpg",
        "clip": "/tmp/test_clip.mp4",
    }
    print("Testing scene analyzer...")
