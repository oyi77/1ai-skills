"""
Vision Detector — Auto-detect product type from image
Uses NVIDIA LLM to analyze product photo and suggest category + style
"""

import os, json, urllib.request, urllib.error, base64
from prompt_library import CATEGORIES, STYLES

NVIDIA_KEY = os.environ.get("NVIDIA_API_KEY")


def detect_product(image_path: str) -> dict:
    """
    Analyze product image and return:
    - category (best match)
    - style (recommended)
    - product_desc (short description)
    - confidence (high/medium/low)
    """
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    categories_str = ", ".join([f"{k} ({v['desc']})" for k, v in CATEGORIES.items()])
    styles_str = ", ".join([f"{k} ({v['desc']})" for k, v in STYLES.items()])

    prompt = f"""Analyze this product image and respond in JSON only.

Categories available: {categories_str}
Styles available: {styles_str}

Respond ONLY with this JSON (no markdown, no explanation):
{{
  "category": "one of the category keys",
  "style_recommendation": "one of the style keys that fits this product best",
  "product_desc": "short 5-10 word description of what you see",
  "product_name": "guessed product name or type",
  "confidence": "high or medium or low",
  "reason": "1 sentence why you chose this category"
}}"""

    payload = json.dumps({
        "model": "meta/llama-3.2-11b-vision-instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
                    {"type": "text", "text": prompt}
                ]
            }
        ],
        "max_tokens": 400,
        "temperature": 0.1
    }).encode()

    headers = {
        "Authorization": f"Bearer {NVIDIA_KEY}",
        "Content-Type": "application/json"
    }

    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            content = data["choices"][0]["message"]["content"].strip()
            # Clean up any markdown
            content = content.replace("```json", "").replace("```", "").strip()
            result = json.loads(content)
            return result
    except Exception as e:
        # Fallback: return unknown
        return {
            "category": None,
            "style_recommendation": "dark_moody",
            "product_desc": "product",
            "product_name": "Unknown product",
            "confidence": "low",
            "reason": f"Could not analyze: {str(e)}"
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = detect_product(sys.argv[1])
        print(json.dumps(result, indent=2))
