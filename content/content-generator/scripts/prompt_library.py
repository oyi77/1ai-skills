"""
Prompt Library — Content Generator
Organized by: Product Category × Visual Style
Updated: 2026-02-27

Usage:
    from prompt_library import get_prompt, CATEGORIES, STYLES
    prompt = get_prompt("minuman", "dark_moody", "image")
"""

# ─── CATEGORIES ───────────────────────────────────────────────────────
CATEGORIES = {
    "minuman": {
        "label": "🍹 Minuman",
        "desc": "Jus, kopi, boba, smoothie, suplemen cair",
    },
    "makanan": {"label": "🍔 Makanan", "desc": "Snack, frozen food, produk kemasan"},
    "beauty": {"label": "💄 Beauty", "desc": "Skincare, makeup, parfum, haircare"},
    "elektronik": {"label": "📱 Elektronik", "desc": "Gadget, aksesoris, wearable"},
    "fashion": {"label": "👗 Fashion", "desc": "Pakaian, sepatu, tas, aksesoris"},
    "suplemen": {"label": "💊 Suplemen", "desc": "Vitamin, protein, herbal, wellness"},
}

# ─── STYLES ───────────────────────────────────────────────────────────
STYLES = {
    "dark_moody": {
        "label": "🖤 Dark & Moody",
        "desc": "Dramatis, mewah, premium vibes",
    },
    "clean_white": {
        "label": "🤍 Clean Studio",
        "desc": "Bersih, minimalis, profesional",
    },
    "luxury": {"label": "✨ Luxury Gold", "desc": "Elegan, gold accent, high-end"},
    "splash": {"label": "💥 Splash Action", "desc": "Dinamis, air/cairan berterbangan"},
    "lifestyle": {"label": "🌿 Lifestyle", "desc": "Natural, relatable, human touch"},
}

# ─── FORMATS ──────────────────────────────────────────────────────────
FORMATS = {
    "foto": {"label": "🖼️ Foto", "desc": "1 gambar produk berkualitas tinggi"},
    "video_15s": {"label": "📱 Video 15s", "desc": "Short-form, story/reels"},
    "video_30s": {"label": "🎬 Video 30s", "desc": "Mid-form, iklan standar"},
    "tiktok_60s": {"label": "🎵 TikTok 60s", "desc": "Full storytelling, viral format"},
}

# ─── HYPERREALISTIC SUFFIX ────────────────────────────────────────────
HR_SUFFIX = (
    ", hyperrealistic photography, ultra detailed, "
    "professional commercial photography, 8K resolution, "
    "sharp focus, perfect exposure, film grain texture"
)

CAMERA_PORTRAIT = ", Sony A7III 85mm f/1.4, bokeh background, RAW photo"
CAMERA_PRODUCT = ", Canon EOS R5 100mm macro, studio strobe lighting, RAW photo"
CAMERA_LIFESTYLE = ", Fujifilm X-T4 35mm f/2, natural light, RAW photo"


# ─── PROMPT LIBRARY ───────────────────────────────────────────────────
LIBRARY = {
    # ══════════════════════════════════════════════════════════════════
    # 🍹 MINUMAN
    # ══════════════════════════════════════════════════════════════════
    "minuman": {
        "dark_moody": {
            "image": (
                "dramatic dark moody product photography of {product_desc}, "
                "placed on wet black marble surface, water droplets on glass, "
                "deep shadows with single dramatic side light, "
                "dark charcoal background, rich saturated colors, "
                "luxury beverage commercial style" + CAMERA_PRODUCT + HR_SUFFIX
            ),
            "i2v": (
                "slow liquid ripple inside glass, condensation droplets sliding down, "
                "dramatic light rays cutting through liquid, cinematic slow motion, "
                "luxury commercial movement"
            ),
        },
        "clean_white": {
            "image": (
                "clean minimalist product photography of {product_desc}, "
                "pure white background, soft diffused studio lighting, "
                "crisp shadows, professional beverage commercial, "
                "bright and fresh mood, glass reflection visible"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": (
                "gentle condensation forming on glass, soft light glow pulsing, "
                "product slowly rotating 360 degrees, clean studio movement"
            ),
        },
        "luxury": {
            "image": (
                "ultra luxury product photography of {product_desc}, "
                "gold and black backdrop, gold foil reflections, "
                "premium packaging highlighted, royal presentation, "
                "velvet surface, soft gold bokeh particles floating"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": (
                "golden particles floating upward, luxurious slow pour of liquid, "
                "gold light rays sweeping across product, premium cinematic reveal"
            ),
        },
        "splash": {
            "image": (
                "high-speed splash photography of {product_desc}, "
                "dramatic liquid explosion frozen in time, "
                "colorful splashing liquid surrounding product, "
                "black background, dramatic studio strobe lighting, "
                "droplets sharp and detailed mid-air" + CAMERA_PRODUCT + HR_SUFFIX
            ),
            "i2v": (
                "liquid splashing dramatically around product, droplets flying in slow motion, "
                "high-speed camera effect, dynamic energetic movement"
            ),
        },
        "lifestyle": {
            "image": (
                "lifestyle photography of {product_desc} in natural setting, "
                "person holding drink in cafe or outdoor setting, "
                "warm golden hour light, bokeh background, "
                "candid natural moment, relatable everyday scene"
                + CAMERA_LIFESTYLE
                + HR_SUFFIX
            ),
            "i2v": (
                "gentle hand picking up drink, warm sunlight shifting, "
                "natural relaxed movement, authentic lifestyle feel"
            ),
        },
    },
    # ══════════════════════════════════════════════════════════════════
    # 🍔 MAKANAN
    # ══════════════════════════════════════════════════════════════════
    "makanan": {
        "dark_moody": {
            "image": (
                "moody food photography of {product_desc}, "
                "rustic dark wood table, dramatic side lighting, "
                "steam rising, rich textures visible, "
                "restaurant quality plating, dark atmospheric background"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": "steam slowly rising from food, candle flickering in background, moody atmospheric",
        },
        "clean_white": {
            "image": (
                "clean food photography of {product_desc}, "
                "white ceramic plate, bright natural lighting, "
                "minimalist food styling, fresh ingredients scattered, "
                "food blog editorial style" + CAMERA_PRODUCT + HR_SUFFIX
            ),
            "i2v": "gentle camera slow zoom into food, fresh ingredients floating in, bright clean movement",
        },
        "luxury": {
            "image": (
                "luxury fine dining photography of {product_desc}, "
                "premium restaurant table setting, gold cutlery, "
                "elegant plating with microgreens, candlelight ambiance"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": "elegant sauce drizzle in slow motion, gold light reflecting, premium reveal movement",
        },
        "splash": {
            "image": (
                "dynamic action food photography of {product_desc}, "
                "ingredients flying and falling dramatically, "
                "frozen mid-air ingredients, high-speed capture, "
                "dramatic black background, studio strobe" + CAMERA_PRODUCT + HR_SUFFIX
            ),
            "i2v": "ingredients dramatically falling and splashing, dynamic high energy food movement",
        },
        "lifestyle": {
            "image": (
                "lifestyle food photography of {product_desc}, "
                "cozy home kitchen setting, natural window light, "
                "hands reaching in, warm family atmosphere"
                + CAMERA_LIFESTYLE
                + HR_SUFFIX
            ),
            "i2v": "hand reaching to grab food naturally, warm kitchen light shifting",
        },
    },
    # ══════════════════════════════════════════════════════════════════
    # 💄 BEAUTY
    # ══════════════════════════════════════════════════════════════════
    "beauty": {
        "dark_moody": {
            "image": (
                "dramatic beauty product photography of {product_desc}, "
                "dark marble or black velvet surface, "
                "single spotlight creating deep shadows, "
                "luxury cosmetics editorial style, glossy reflections"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": "cream or liquid texture slowly swirling, dramatic light shift revealing product, luxury reveal",
        },
        "clean_white": {
            "image": (
                "clean minimalist beauty photography of {product_desc}, "
                "white background, soft diffused natural light, "
                "clinical clean aesthetic, skincare routine styling, "
                "fresh flowers or leaves as accents" + CAMERA_PRODUCT + HR_SUFFIX
            ),
            "i2v": "soft petals falling around product, gentle rotation, fresh clean movement",
        },
        "luxury": {
            "image": (
                "ultra luxury beauty photography of {product_desc}, "
                "gold and rose gold accents, pearl and crystal reflections, "
                "premium packaging close-up, opulent styling"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": "golden shimmer particles floating around product, luxury unboxing reveal movement",
        },
        "splash": {
            "image": (
                "creative beauty splash photography of {product_desc}, "
                "serum or cream dramatically splashing, "
                "liquid texture frozen in motion, colorful product tones"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": "cream or serum dramatically flowing and splashing, slow motion skincare action",
        },
        "lifestyle": {
            "image": (
                "lifestyle beauty photography of {product_desc}, "
                "used in morning skincare routine setting, "
                "natural bathroom light, clean vanity background, "
                "real skin texture, authentic feel" + CAMERA_LIFESTYLE + HR_SUFFIX
            ),
            "i2v": "hand applying product naturally, soft morning light, authentic skincare moment",
        },
    },
    # ══════════════════════════════════════════════════════════════════
    # 📱 ELEKTRONIK
    # ══════════════════════════════════════════════════════════════════
    "elektronik": {
        "dark_moody": {
            "image": (
                "dramatic tech product photography of {product_desc}, "
                "dark background with subtle blue/purple neon glow, "
                "futuristic aesthetic, glass surface reflection, "
                "premium tech commercial style" + CAMERA_PRODUCT + HR_SUFFIX
            ),
            "i2v": "neon light trail sweeping across product, screen glowing on, dramatic tech reveal",
        },
        "clean_white": {
            "image": (
                "clean minimalist tech photography of {product_desc}, "
                "pure white background, Apple-style commercial aesthetic, "
                "precise shadow, product floating or on surface"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": "clean 360 product rotation, crisp shadow rotating, Apple-style reveal movement",
        },
        "luxury": {
            "image": (
                "premium luxury tech photography of {product_desc}, "
                "dark background with gold and chrome reflections, "
                "premium materials highlighted, aspirational positioning"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": "premium slow reveal with light sweep, luxury product showcase rotation",
        },
        "splash": {
            "image": (
                "dynamic tech product photography of {product_desc}, "
                "product launching from explosion of light particles, "
                "energy burst background, dramatic commercial visual"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": "particle burst exploding from product, energy light trails, dynamic tech movement",
        },
        "lifestyle": {
            "image": (
                "lifestyle tech photography of {product_desc} in use, "
                "person using product in modern workspace or outdoor, "
                "natural interaction, relatable modern lifestyle"
                + CAMERA_LIFESTYLE
                + HR_SUFFIX
            ),
            "i2v": "hands naturally interacting with product, real-world usage scene, authentic feel",
        },
    },
    # ══════════════════════════════════════════════════════════════════
    # 👗 FASHION
    # ══════════════════════════════════════════════════════════════════
    "fashion": {
        "dark_moody": {
            "image": (
                "editorial fashion photography of {product_desc}, "
                "dramatic studio lighting, dark background, "
                "high fashion magazine aesthetic, "
                "strong shadows and highlights, professional fashion shoot"
                + CAMERA_PORTRAIT
                + HR_SUFFIX
            ),
            "i2v": "fabric flowing dramatically in wind, editorial movement, fashion film aesthetic",
        },
        "clean_white": {
            "image": (
                "clean editorial fashion photography of {product_desc}, "
                "bright white studio background, "
                "professional fashion catalog aesthetic, "
                "clean lines, product details clearly visible"
                + CAMERA_PORTRAIT
                + HR_SUFFIX
            ),
            "i2v": "clean model turn and pose, fabric movement, catalog style rotation",
        },
        "luxury": {
            "image": (
                "luxury fashion photography of {product_desc}, "
                "high-end boutique setting or luxury backdrop, "
                "Vogue magazine editorial quality, "
                "elegant sophisticated styling" + CAMERA_PORTRAIT + HR_SUFFIX
            ),
            "i2v": "elegant slow movement, luxury fabric draping, high fashion film movement",
        },
        "splash": {
            "image": (
                "dynamic action fashion photography of {product_desc}, "
                "movement frozen mid-air, fabric flying, "
                "energetic pose, dramatic lighting, "
                "editorial action shot" + CAMERA_PORTRAIT + HR_SUFFIX
            ),
            "i2v": "dynamic jump or spin, fabric flying in slow motion, energetic fashion movement",
        },
        "lifestyle": {
            "image": (
                "lifestyle street fashion photography of {product_desc}, "
                "urban outdoor setting, golden hour light, "
                "candid natural pose, authentic style" + CAMERA_LIFESTYLE + HR_SUFFIX
            ),
            "i2v": "casual natural walking movement, street light shifting, authentic lifestyle feel",
        },
    },
    # ══════════════════════════════════════════════════════════════════
    # 💊 SUPLEMEN
    # ══════════════════════════════════════════════════════════════════
    "suplemen": {
        "dark_moody": {
            "image": (
                "dramatic supplement product photography of {product_desc}, "
                "dark background with teal/blue accent lighting, "
                "pills or capsules artfully arranged, "
                "premium health brand aesthetic, strong and powerful mood"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": "capsules or pills dramatically arranged, powerful light sweep, premium health reveal",
        },
        "clean_white": {
            "image": (
                "clean clinical supplement photography of {product_desc}, "
                "white background, clinical trust-building aesthetic, "
                "ingredients laid out naturally, medical-grade presentation"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": "clean minimal product rotation, ingredient elements floating in, clinical movement",
        },
        "luxury": {
            "image": (
                "luxury wellness photography of {product_desc}, "
                "premium spa-like setting, natural elements like herbs and botanicals, "
                "gold and earth tones, high-end wellness brand aesthetic"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": "botanical elements floating gracefully, luxury wellness reveal, golden particles",
        },
        "splash": {
            "image": (
                "dynamic supplement photography of {product_desc}, "
                "capsules bursting with ingredient particles, "
                "powerful energy visualization, "
                "ingredients dramatically exploding outward"
                + CAMERA_PRODUCT
                + HR_SUFFIX
            ),
            "i2v": "capsule bursting with ingredient particles in slow motion, powerful energy reveal",
        },
        "lifestyle": {
            "image": (
                "lifestyle wellness photography of {product_desc}, "
                "active healthy lifestyle setting, morning routine, "
                "gym or outdoor context, real person using product, "
                "motivational and inspiring mood" + CAMERA_LIFESTYLE + HR_SUFFIX
            ),
            "i2v": "active lifestyle movement, morning routine moment, inspiring natural motion",
        },
    },
}


# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────
def get_prompt(
    category: str,
    style: str,
    format_type: str = "image",
    product_desc: str = "the product",
) -> dict:
    """
    Get image + i2v prompts for a category/style combination.

    Args:
        category: One of CATEGORIES keys (minuman, makanan, beauty, etc.)
        style: One of STYLES keys (dark_moody, clean_white, etc.)
        format_type: 'foto', 'video_15s', 'video_30s', 'tiktok_60s'
        product_desc: Short description of the actual product

    Returns:
        dict with 'image' and 'i2v' prompts, model recommendations
    """
    if category not in LIBRARY:
        raise ValueError(
            f"Category '{category}' not found. Available: {list(LIBRARY.keys())}"
        )
    if style not in LIBRARY[category]:
        raise ValueError(f"Style '{style}' not found for {category}.")

    prompts = LIBRARY[category][style]
    image_prompt = prompts["image"].replace("{product_desc}", product_desc)
    i2v_prompt = prompts.get("i2v", "gentle product movement, cinematic slow motion")

    # Select right image model (SD3 for fashion/lifestyle with people, Flux for products)
    needs_person = category in ("fashion",) or style == "lifestyle"
    image_model = (
        "stabilityai/stable-diffusion-3-medium"
        if needs_person
        else "black-forest-labs/flux.1-dev"
    )
    video_model = "seedance-1-0-pro-250528"

    return {
        "image_prompt": image_prompt,
        "i2v_prompt": i2v_prompt,
        "image_model": image_model,
        "video_model": video_model,
        "format": format_type,
        "category": category,
        "style": style,
    }


def list_options():
    """Print all available categories and styles"""
    print("\n📦 CATEGORIES:")
    for k, v in CATEGORIES.items():
        print(f"  {v['label']} [{k}] — {v['desc']}")
    print("\n🎨 STYLES:")
    for k, v in STYLES.items():
        print(f"  {v['label']} [{k}] — {v['desc']}")
    print("\n📤 FORMATS:")
    for k, v in FORMATS.items():
        print(f"  {v['label']} [{k}] — {v['desc']}")


if __name__ == "__main__":
    list_options()
    print("\n--- Test: minuman × dark_moody ---")
    p = get_prompt("minuman", "dark_moody", "video_15s", "botol jus mangga premium")
    print(f"Image Model: {p['image_model']}")
    print(f"Image Prompt:\n{p['image_prompt']}\n")
    print(f"I2V Prompt:\n{p['i2v_prompt']}")
