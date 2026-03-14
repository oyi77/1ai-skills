#!/usr/bin/env python3
"""
Content Validation Workflow - Sample Review → Approval → Batch Production
Generate 1 sample → Human Review → Approved → Scale 50-100 pieces
"""

import json
from pathlib import Path
from datetime import datetime

# Setup paths
workspace = Path.home() / ".openclaw" / "workspace"
samples_dir = workspace / "content" / "samples"
approvals_file = workspace / "content" / "approvals.json"
scheduled_file = workspace / "content" / "scheduled.json"

# Create directories
samples_dir.mkdir(parents=True, exist_ok=True)

# Products
PRODUCTS = {
    "guru_pintar_ai": {
        "name": "Guru Pintar AI",
        "price": "GRATIS",
        "url": "https://lynk.id/jendralbot/6821op5e24kn",
        "hashtags": "#free #AItraining #belajarAI #AIindonesia",
    },
    "belanja_duit_balik": {
        "name": "Belanja Duit Balik",
        "price": "GRATIS",
        "url": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
        "hashtags": "#cashback #belanja #hemat #smartshopping",
    },
    "ai_content_pro": {
        "name": "AI Content Pro",
        "price": "Rp 89.000",
        "url": "https://lynk.id/jendralbot/d70eo2x45em5",
        "hashtags": "#AIcontent #AIautomation #contentcreation",
    },
    "studio_marketplace_pro": {
        "name": "Studio Marketplace Pro",
        "price": "Rp 75.000",
        "url": "https://lynk.id/jendralbot/emne05mm7v25",
        "hashtags": "#ecommerce #productphoto #jualanonline",
    },
    "mesin_cetak_kuliner": {
        "name": "Mesin Cetak Kuliner",
        "price": "Rp 75.000",
        "url": "https://lnkd.in/mesin_cetak",
        "hashtags": "#kuliner #foodphotography #restaurant",
    }
}

def generate_sample(product_key, content_type, variant=1):
    """Generate 1 sample content for review"""
    product = PRODUCTS[product_key]
    
    sample_id = f"{product_key}_{content_type}_v{variant}"
    
    # Generate script based on product & content type
    if "faceless" in content_type:
        script = generate_faceless_script(product, variant)
    else:
        script = generate_regular_script(product, content_type, variant)
    
    quality_checklist = {
        "image_quality": "⚠️ PENDING",
        "text_overlay": "⚠️ PENDING",
        "hook_strength": "⚠️ PENDING",
        "cta_clarity": "⚠️ PENDING",
        "brand_voice": "⚠️ PENDING"
    }
    
    # Save sample to file
    sample_file = samples_dir / f"{sample_id}.txt"
    with open(sample_file, "w") as f:
        f.write(f"=== SAMPLE: {product['name']} - {content_type} v{variant} ===\n\n")
        f.write(f"Product: {product['name']}\n")
        f.write(f"URL: {product['url']}\n")
        f.write(f"Hashtags: {product['hashtags']}\n\n")
        f.write("=" * 80 + "\n")
        f.write("SCRIPT:\n")
        f.write("=" * 80 + "\n")
        f.write(script + "\n\n")
        f.write("=" * 80 + "\n")
        f.write("QUALITY CHECKLIST:\n")
        f.write("=" * 80 + "\n")
        for key, value in quality_checklist.items():
            f.write(f"{key:20s}: {value}\n")
    
    return {
        "sample_id": sample_id,
        "file_path": str(sample_file),
        "script": script,
        "checklist": quality_checklist,
        "product": product,
        "status": "PENDING"
    }

def generate_faceless_script(product, variant=1):
    """Generate faceless video script"""
    hooks = {
        1: "🔥 STOP! Konten manual makan waktu 4 jam/post!",
        2: "💡 5 Tips Hemat Belanja Hari Ini!",
        3: "📊 Data shows 90% content creators fail without AI"
    }
    
    body = f"""
Dulu saya {product['name']} manual prosesnya lama.
Writing caption + edit gambar + posting = 4 jam/post!

Solusi: {product['name']} - {product['price']}
Ide 5 menit + caption 1 menit + edit 1 menit = 8 menit/post

ROI: 90 jam/hari -> 360 konten/bulan

CTA: Start dengan GRATIS, level-up ke {product['url']}
"""
    
    visual = f"""
HOOK (0-3s): Text overlay centered bold white - "{hooks[variant]}"

BODY (3-12s): Voice over explaining solution
Text overlays: 2-3 key points
B-roll: Screen recording showing product interface

CTA (13-15s): Product link centered
Fade to black
"""
    
    audio = f"""
Voice: Energetic & friendly
Music: Upbeat instrumental (Spotify free tier)
Tempo: 120-140 BPM
Volume: 30-40% of voice
"""
    
    return f"HOOK:\n{hooks[variant]}\n\nBODY:\n{body.strip()}\n\nVISUAL:\n{visual.strip()}\n\nAUDIO:\n{audio.strip()}"

def generate_regular_script(product, content_type, variant=1):
    """Generate regular (non-faceless) content"""
    hooks = {
        1: "Jangan bikin konten manual! Ini cara cepatnya",
        2: "5 tips yang saya buat ribuan followers",
        3: "Ini yang bikin content creator berhasil"
    }
    
    caption = f"""
{hooks[variant]}

{product['name']} {product['price']}
Full automation untuk content creator

💰 Ide: 5 menit
⚡ Caption: 1 menit
🎨 Edit: 1 menit
⏰ Posting: 1 menit

Result: 8 menit/post x 90 posts/bulan = 720 menit/hari!

CTA: {product['url']}

{product['hashtags']}
"""
    
    return caption.strip()

def request_approval(product_key, content_type, variant=1):
    """Send sample for human review"""
    sample = generate_sample(product_key, content_type, variant)
    
    approval_request = f"""
{'=' * 80}
📋 REVIEW SAMP KONTEN
{'=' * 80}

Product: {sample['product']['name']}
Type: {content_type} v{variant}
Status: {sample['status']}

{'=' * 80}
QUALITY CHECKLIST
{'=' * 80}

✅ Image Quality   : [ ] CLEAR & HIGH RESOLUSI
✅ Text Overlay    : [ ] VISIBLE & READABLE
✅ Hook Strength   : [ ] STRONG in first 3 seconds
✅ CTA Clarity     : [ ] CLEAR at end
✅ Brand Voice     : [ ] MATCHES Jendralbot tone

{'=' * 80}
REVIEW INSTRUCTIONS
{'=' * 80}

Cek file: {sample['file_path']}

Respon dengan salah satu:

1. 'ACC'          → TOLAK batch production sekarang
2. 'EDIT [instruksi]' → Regulate sample dengan instruksi spesifik
   Contoh: 'EDIT Text overlay perlu putih lebih terang'

3. 'SKIP'         → Skip ke sampel lain biarkan pending
4. 'REJECT'       → Tolak sampel jangan di-scale

{'=' * 80}
Catatan:
- Konten di-save ke: {sample['file_path']}
- Approval disimpan ke: {approvals_file}
- Setelah ACC: batch production 50-100 pieces

{'=' * 80}
"""
    
    return approval_request

def save_approval(sample_id, status, feedback=""):
    """Save approval status to file"""
    
    # Load existing approvals
    try:
        with open(approvals_file, "r") as f:
            approvals = json.load(f)
    except FileNotFoundError:
        approvals = {}
    
    # Save new approval
    approvals[sample_id] = {
        "status": status,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat()
    }
    
    # Write to file
    with open(approvals_file, "w") as f:
        json.dump(approvals, f, indent=2)
    
    print(f"✅ Approval saved: {sample_id} = {status}")

def generate_batch_from_approved(product_key, content_type, quantity=50):
    """Generate batch content FROM approved samples"""
    
    # Load approved samples
    try:
        with open(approvals_file, "r") as f:
            approvals = json.load(f)
    except FileNotFoundError:
        print("❌ No approvals found. Request review first.")
        return []
    
    # Find approved sample for this product/type
    sample_id = f"{product_key}_{content_type}_v1"
    approval = approvals.get(sample_id, {})
    
    if approval.get("status") != "APPROVED":
        print(f"❌ Sample {sample_id} not approved. Status: {approval.get('status')}")
        return []
    
    print(f"✅ Generating batch: {quantity} pieces from {sample_id}")
    
    # Load original sample
    sample_file = samples_dir / f"{sample_id}.txt"
    with open(sample_file, "r") as f:
        original_sample = f.read()
    
    # Generate batch variations
    batch = []
    for i in range(quantity):
        variant_id = f"{sample_id}_batch_{i+1}"
        
        # For batch, we'd normally create variations
        # For now, save placeholder
        batch.append({
            "variant_id": variant_id,
            "sample_base": sample_id,
            "quantity": i+1,
            "status": "QUEUED"
        })
    
    return batch

def show_pending_reviews():
    """Show all samples pending review"""
    try:
        with open(approvals_file, "r") as f:
            approvals = json.load(f)
    except FileNotFoundError:
        approvals = {}
    
    print("\n" + "=" * 80)
    print("PENDING REVIEWS")
    print("=" * 80)
    
    pending = [k for k, v in approvals.items() if v.get("status") == "PENDING"]
    
    if not pending:
        print("No pending reviews")
    
    for sample_id in pending:
        print(f"- {sample_id}")

def list_all_samples():
    """List all generated samples"""
    print("\n" + "=" * 80)
    print("ALL SAMPLES GENERATED")
    print("=" * 80)
    
    for file in samples_dir.glob("*_v*.txt"):
        print(f"- {file.stem}")
    
    # Show approval status
    try:
        with open(approvals_file, "r") as f:
            approvals = json.load(f)
        
        print("\n" + "=" * 80)
        print("APPROVAL STATUS")
        print("=" * 80)
        
        for sample_id, status_info in approvals.items():
            status = status_info.get("status", "UNKNOWN")
            feedback = status_info.get("feedback", "")
            print(f"- {sample_id}: {status}")
            if feedback:
                print(f"  Feedback: {feedback}")
    except FileNotFoundError:
        print("No approval status recorded yet.")

def main():
    print("=" * 80)
    print("CONTENT VALIDATION WORKFLOW")
    print("=" * 80)
    print()
    print("Workflow:")
    print("1. Generate 1 sample per product")
    print("2. Request approval → ACC/EDIT/SKIP/REJECT")
    print("3. Generate batch from approved samples (50-100 pieces)")
    print()
    
    # Demo: Generate sample for Guru Pintar AI
    print("=" * 80)
    print("STEP 1: GENERATING SAMPLES")
    print("=" * 80)
    print()
    
    request = request_approval("guru_pintar_ai", "faceless_info_benefit", 1)
    print(request)
    
    print()
    print("=" * 80)
    print("STEP 2: NEXT ACTIONS")
    print("=" * 80)
    print()
    print("To approve/regulate sample:")
    print("  python3 scripts/content_validator.py --approve <sample_id> ACC")
    print("  python3 scripts/content_validator.py --approve <sample_id> EDIT [instruksi]")
    print()
    print("To generate batch after approval:")
    print("  python3 scripts/content_validator.py --batch guru_pintar_ai faceless_info_benefit 50")
    print()
    print("To view all samples:")
    print("  python3 scripts/content_validator.py --list")
    print()
    print("=" * 80)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--list":
            list_all_samples()
        
        elif arg == "--pending":
            show_pending_reviews()
        
        elif arg == "--approve":
            if len(sys.argv) >= 3:
                sample_id = sys.argv[2]
                status = sys.argv[3] if len(sys.argv) > 3 else "ACC"
                feedback = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
                save_approval(sample_id, status, feedback)
        
        elif arg == "--batch":
            if len(sys.argv) >= 4:
                product_key = sys.argv[2]
                content_type = sys.argv[3]
                quantity = int(sys.argv[4]) if len(sys.argv) > 4 else 50
                generate_batch_from_approved(product_key, content_type, quantity)
        
        else:
            print("Unknown command. Use: --list, --pending, --approve, --batch")
    else:
        main()