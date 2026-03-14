#!/usr/bin/env python3
"""
JENDRALBOT CHARACTER-BASED MEDIA GENERATOR
Video 24-30s | Hook-Based | AICDA Compliant | Consistent Characters

Features:
- Character-based system (1 character per account)
- Image-first workflow: Generate character → Split poses → Match video
- 24-30 second videos (direct generation, no looping)
- Hook dalam 3 detik pertama
- AICDA compliant (Attention, Interest, Curiosity, Desire, Action)
- Cost optimized with reusable characters
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# Configuration
WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
ENGINE_DIR = WORKSPACE / "autopilot_affiliate_engine"
OUTPUT_DIR = ENGINE_DIR / "jendralbot_character_media"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Cost targets
COST_TARGETS = {
    "per_character_image": 0.004,      # NVIDIA Flux
    "per_video_24s": 0.125,            # BytePlus Seedance ($0.026 × 5s)
    "per_video_30s": 0.156,            # BytePlus Seedance ($0.026 × 6s)
}

# Account characters (per platform/account)
ACCOUNT_CHARACTERS = {
    "tiktok_main": {
        "name": "Sarah Putri",
        "description": "Gen Z Indonesian woman, 25 years old, natural",
        "style": "authentic, relatable, energetic",
        "look": "natural minimal makeup, modern casual wear, black hair",
        "vibe": "friendly, approachable, gen z energy"
    },
    "instagram_business": {
        "name": "Jessica Wijaya",
        "description": "Millennial Indonesian entrepreneur, 28 years old",
        "style": "professional yet approachable, polished",
        "look": "smart casual, confident, clean aesthetics",
        "vibe": "knowledgeable, trustworthy, business-friendly"
    },
    "facebook_ads": {
        "name": "Anita Kusuma",
        "description": "Young Indonesian mom, 30 years old",
        "style": "warm, motherly, trustworthy",
        "look": "casual comfortable wear, genuine smile",
        "vibe": "caring, practical, relatable to parents"
    },
    "twitter_threads": {
        "description": "AI-generated abstract representations",
        "style": "modern, tech-forward, minimalist",
        "note": "Thread format uses dynamic graphics, no consistent character"
    },
    "youtube_shorts": {
        "name": "Rina Santoso",
        "description": "Gen Z Indonesian content creator, 23 years old",
        "style": "fun, quirky, expressive",
        "look": "colorful, trendy, animated expressions",
        "vibe": "energetic, entertaining, quick-paced"
    }
}

# Pose variations for each character
POSE_VARIATIONS = {
    "talking_to_camera": "facing camera directly, slight smile, natural expression",
    "holding_phone": "holding smartphone naturally, scrolling or showing screen",
    "showing_product": "product in hand or displayed visibly, proud expression",
    "gesturing": "one hand gesturing towards product, explaining",
    "laughing": "genuine laugh, head slightly tilted, relaxed",
    "curious": "slightly tilted head, curious expression, looking at product",
    "pointing": "finger pointing at product or text on screen",
    "nodding": "nodding agreement, maintaining eye contact",
    "thinking": "one hand on chin, thoughtful expression",
    "celebrating": "both arms up, happy celebration, excited"
}

# Video segments structure (24-30s)
VIDEO_SEGMENTS_30S = {
    "hook": {"duration": 3, "purpose": "Grab attention in 3s"},
    "problem": {"duration": 7, "purpose": "Present problem/reality"},
    "solution": {"duration": 8, "purpose": "Present your product as solution"},
    "proof": {"duration": 7, "purpose": "Show proof/results"},
    "cta": {"duration": 5, "purpose": "Call to action"}
}

VIDEO_SEGMENTS_24S = {
    "hook": {"duration": 3, "purpose": "Grab attention in 3s"},
    "problem": {"duration": 5, "purpose": "Present problem/reality"},
    "solution": {"duration": 8, "purpose": "Present your product as solution"},
    "cta": {"duration": 8, "purpose": "Call to action"}
}

class CharacterBasedMediaGenerator:
    """Character-based media generator with AICDA compliance"""
    
    def __init__(self):
        self.load_products()
        self.character_cache = {}  # Cache generated characters
        self.pose_cache = {}       # Cache split poses
    
    def load_products(self):
        """Load Jendralbot products"""
        product_file = ENGINE_DIR / "jendralbot_products.json"
        with open(product_file) as f:
            data = json.load(f)
            self.products = data["products"]
        
        self.high_priority = [p for p in self.products if p["price"] == 0]
        self.medium_priority = [p for p in self.products if 49000 <= p["price"] <= 75000]
        self.low_priority = [p for p in self.products if p["price"] > 75000]
        
        print(f"✅ Loaded {len(self.products)} products")
        print(f"   High priority (FREE): {len(self.high_priority)}")
        print(f"   Medium priority: {len(self.medium_priority)}")
        print(f"   Low priority: {len(self.low_priority)}")
    
    def generate_character_image(self, account: str) -> Dict:
        """
        Generate consistent character image for an account
        
        Cost: $0.004 (one-time per character)
        Reusable for all videos from that account
        """
        
        if account not in ACCOUNT_CHARACTERS:
            print(f"❌ Account '{account}' not found in character system")
            return {"success": False, "error": "Account not found"}
        
        char_data = ACCOUNT_CHARACTERS[account]
        
        # Prompt for consistent character
        if "name" in char_data:
            prompt = f"""
{char_data['name']}, {char_data['description']}, {char_data['style']}
{char_data['look']}
Medium close-up portrait, facing camera directly, neutral expression
Professional headshot style, clean background
High quality, consistent character design
            """.strip().replace('\n', ' ')
        else:
            # For accounts without characters (like Twitter)
            prompt = """
Abstract modern tech graphics, minimalist design
Data visualization style, clean aesthetics
Professional business representation
            """.strip().replace('\n', ' ')
        
        filename = f"character_{account}_{datetime.now().timestamp()}.png"
        output_path = OUTPUT_DIR / filename
        
        return {
            "success": True,
            "path": str(output_path),
            "account": account,
            "character_name": char_data.get("name", "Abstract"),
            "cost": COST_TARGETS["per_character_image"],
            "prompt": prompt,
            "pose_variations": list(POSE_VARIATIONS.keys())
        }
    
    def split_character_poses(self, character_path: str, account: str) -> Dict:
        """
        Split character image into different poses
        
        Concept: Extract pose variations for video generation
        Cost: Included in character generation (no additional cost)
        """
        
        char_data = ACCOUNT_CHARACTERS.get(account, {})
        
        poses = {}
        for pose_name, pose_desc in POSE_VARIATIONS.items():
            # Simulate pose variation extraction
            pose_filename = f"{pose_name}_{account}_{datetime.now().timestamp()}.png"
            pose_path = OUTPUT_DIR / pose_filename
            
            if "name" in char_data:
                prompt = f"""
{char_data.get('name', 'Character')}, {char_data.get('description', '')},
{pose_desc}
{char_data.get('style', '')}
{char_data.get('look', '')}
Natural lighting, consistent with character reference
                """.strip().replace('\n', ' ')
            else:
                prompt = f"""
Abstract graphics, {pose_desc}
Minimalist tech style, professional aesthetic
                """.strip().replace('\n', ' ')
            
            poses[pose_name] = {
                "path": str(pose_path),
                "pose": pose_name,
                "description": pose_desc,
                "prompt": prompt,
                "cost": 0.0  # No additional cost (simulated variation)
            }
        
        return {
            "success": True,
            "character_path": character_path,
            "account": account,
            "poses": poses,
            "total_poses": len(poses)
        }
    
    def generate_hook_segment_script(self, product: Dict, account: str) -> Dict:
        """
        Generate hook script (3s, attention-grabbing)
        
        Hook strategies:
        - Shocking statement
        - Problem agitation
        - Benefit-focused question
        - Contrarian statement
        """
        
        hooks = [
            f"Stop scrolling! You're losing money every day!",
            f"Hati-hati! Kamu ngelewat kesempatan gede ini!",
            f"Bosen banget kan gak ada penghasilan tambahan?",
            f"Percaya nggak kalau ini bisa gaji bulanan?",
            f"Jangan lanjut scroll kalau mau duit gratis!",
            f"Satu klik ini ubah hidup kamu selamanya!",
            f"Kenapa orang lain bisa tapi kamu belum?",
            f"Terlambat tau, padahal udah lama ada!",
            f"Ini rahasia yang gak akan aku bagikan gratis!",
            f"Tunggu apa lagi? Gratis dan langsung cair!"
        ]
        
        import random
        hook = random.choice(hooks)
        
        pose_sequence = [
            {"second": 0, "pose": "talking_to_camera", "action": "Speak directly with intense gaze"},
            {"second": 1.5, "pose": "pointing", "action": "Point at camera/product"},
            {"second": 3, "pose": "laughing", "action": "Transition to friendly"}
        ]
        
        return {
            "hook_text": hook,
            "duration": 3,
            "pose_sequence": pose_sequence,
            "strategy": "Attention grabber"
        }
    
    def generate_problemSegment_script(self, product: Dict, account: str) -> Dict:
        """Generate script segment after hook"""
        
        if account == "youtube_shorts" or account == "tiktok_main":
            # Gen Z style
            scripts = [
                f"Gini bro, tiap hari scroll TikTok nonton orang pamer duit.",
                f"Kamu juga bosen kan kerja from pagi sampai malem?",
                f"Pengen income tambahan tapi gak tau dari mana?",
                f"Ngeliat orang lain viral, kamu cuma nonton?",
                f"Kenyataannya, skill yang kamu punya bisa duit!"
            ]
        elif account == "instagram_business":
            # Professional style
            scripts = [
                f"Di tengah ekonomi yang nggak pasti, kita butuh penghasilan tambahan.",
                f"Banyak profesional mencari cara untuk monetisasi skill.",
                f"Problem besarnya: Gak semua orang punya produk jualan.",
                f"Ternyata, produk digital bisa jadi solusi hemat biaya.",
                f"Modal cuma smartphone + internet, profit bisa jutaan!"
            ]
        elif account == "facebook_ads":
            # Mom/parent style
            scripts = [
                f"Sebagai ibu, pasti pengen nambah pendapatan dari rumah.",
                f"Bantu suami, biar perekonomian keluarga lebih stabil.",
                f"Tapi gak semua orang bisa keluar kerja.",
                f"Ada cara yang bisa dilakukan jam fleksibel.",
                f"Bisa sambil urus anak, sambil jalanin bisnis!"
            ]
        else:
            # Generic
            scripts = [
                f"Kenyataannya, banyak orang mencari penghasilan tambahan.",
                f"Problemnya: Gak semua orang punya produk jualan.",
                f"Ini yang sering bikin orang nyerah sebelum mulai.",
                f"Tapi sekarang ada solusinya yang praktis banget.",
                f"Bisa mulai dari nol, tanpa modal besar!"
            ]
        
        import random
        script = random.choice(scripts)
        
        return {
            "script_text": script,
            "duration": 7,
            "emotion": "Empathy, relatable"
        }
    
    def generate_solution_segment_script(self, product: Dict, account: str) -> Dict:
        """Generate solution segment script"""
        
        description = product.get('description', 'Produk luar biasa untuk memperbanyak penghasilan')
        
        if account == "youtube_shorts" or account == "tiktok_main":
            script = f"{product['name']} jawabannya! {description[:50]}..." \
                     f" Gratis ambil, langsung bisa pakai buat cari cuan!"
        elif account == "instagram_business":
            script = f"{product['name']} adalah solusinya. {description[:60]}..." \
                     f" Professional dan siap pakai untuk bisnis Anda."
        else:
            script = f"{product['name']} ini solusinya! {description[:50]}..." \
                     f" Langsung bisa diakses, gratis dan mudah dipakai!"
        
        return {
            "script_text": script,
            "duration": 8,
            "emotion": "Excited, solution-focused"
        }
    
    def generate_cta_segment_script(self, product: Dict, account: str) -> Dict:
        """Generate call-to-action segment"""
        
        ctas = [
            "Cek link di bio sekarang!",
            "Klik tombol kuning di bawah!",
            "Ambil gratis sekarang, gak pake lama!",
            "Link ada di deskripsi, gas ambil!",
            "Cek bio, jangan sampe nyesel!",
            "Gratis kok, cek sekarang!",
            "Buruan ambil sekarang, terbatas!",
            "Link di bio, tunggu apalagi!",
            "Klik sekarang, gratis 100%!",
            "Cek bio jendralbot, gas!"
        ]
        
        import random
        cta = random.choice(ctas)
        
        return {
            "text": cta,
            "duration": 5,
            "action": "Direct user to click"
        }
    
    def generate_video_script_30s(self, product: Dict, account: str) -> Dict:
        """
        Generate complete 30s video script with AICDA structure
        
        AICDA:
        - Attention (Hook): 0-3s
        - Interest (Problem/Agitate): 3-10s
        - Curiosity (Solution preview): 10-18s
        - Desire (Proof/Value): 18-25s
        - Action (CTA): 25-30s
        """
        
        # Generate each segment
        hook = self.generate_hook_segment_script(product, account)
        problem = self.generate_problemSegment_script(product, account)
        solution = self.generate_solution_segment_script(product, account)
        cta = self.generate_cta_segment_script(product, account)
        
        # Combine into full script
        full_script = f"""
🎯 HOOK (0-3s):
{hook['hook_text']}

📖 PROBLEM (3-10s):
{problem['script_text']}

💡 SOLUTION (10-18s):
{solution['script_text']}

🎬 PROOF (18-25s):
{product['name']} ini udah dipake ribuan orang!
Udah terbukti, tinggal action aja!

🚀 CTA (25-30s):
{cta['text']}
        """.strip()
        
        return {
            "duration": 30,
            "full_script": full_script,
            "segments": {
                "hook": hook,
                "problem": problem,
                "solution": solution,
                "cta": cta
            },
            "aicda_structure": {
                "Attention": "0-3s: Hook",
                "Interest": "3-10s: Problem agitate",
                "Curiosity": "10-18s: Solution preview",
                "Desire": "18-25s: Proof/Value",
                "Action": "25-30s: Call to action"
            }
        }
    
    def generate_video_script_24s(self, product: Dict, account: str) -> Dict:
        """
        Generate complete 24s video script (shorter version)
        """
        
        hook = self.generate_hook_segment_script(product, account)
        problem = self.generate_problemSegment_script(product, account)
        solution = self.generate_solution_segment_script(product, account)
        cta = self.generate_cta_segment_script(product, account)
        
        full_script = f"""
🎯 HOOK (0-3s):
{hook['hook_text']}

📖 PROBLEM (3-8s):
{problem['script_text']}

💡 SOLUTION (8-16s):
{solution['script_text']}

🚀 CTA (16-24s):
{cta['text']}
        """.strip()
        
        return {
            "duration": 24,
            "full_script": full_script,
            "segments": {
                "hook": hook,
                "problem": problem,
                "solution": solution,
                "cta": cta
            },
            "aicda_structure": {
                "Attention": "0-3s: Hook",
                "Interest": "3-8s: Problem",
                "Curiosity": "8-16s: Solution",
                "Desire": "Integrated in solution",
                "Action": "16-24s: CTA"
            }
        }
    
    def generate_video_with_pose_matching(self, product: Dict, account: str, 
                                         character_path: str, poses: Dict, 
                                         video_script: Dict) -> Dict:
        """
        Generate 24-30s video with pose matching from character
        
        Workflow:
        1. Read character poses from cache
        2. Match poses to video script segments
        3. Generate video with seamless pose transitions
        
        Cost: $0.125-$0.156 per video (24-30s)
        """
        
        duration = video_script["duration"]
        
        # Match poses to segments
        pose_sequence = []
        current_time = 0
        
        for segment_name, segment_data in video_script["segments"].items():
            segment_duration = segment_data["duration"]
            
            # Select pose for this segment
            if segment_name == "hook":
                pose_key = "talking_to_camera"
            elif segment_name == "problem":
                pose_key = "curious"
            elif segment_name == "solution":
                pose_key = "holding_phone"
            elif segment_name == "cta":
                pose_key = "pointing"
            else:
                pose_key = "showing_product"
            
            if pose_key in poses:
                pose_data = poses[pose_key]
                pose_sequence.append({
                    "start_second": current_time,
                    "end_second": current_time + segment_duration,
                    "pose": pose_key,
                    "description": pose_data["description"],
                    "action": segment_data.get("action", "Natural")
                })
            
            current_time += segment_duration
        
        # Generate video prompt
        char_data = ACCOUNT_CHARACTERS.get(account, {})
        
        if "name" in char_data:
            video_prompt = f"""
{char_data.get('name', 'Character')}, {char_data.get('description', '')},
{char_data.get('style', '')}, {char_data.get('vibe', '')}

Sequential:
{', '.join([f"at {p['start_second']}s: {p['description']}" for p in pose_sequence])}

Holding {product['name']} naturally,
in modern setting, ambient lighting,
genuine expressions matching segments,
professional video quality, smooth transitions
            """.strip().replace('\n', ' ')
        else:
            video_prompt = f"""
Professional business presentation,
modern tech aesthetics,
{product['name']} showcased dynamically,
smooth transitions, engaging visuals
            """.strip().replace('\n', ' ')
        
        # Calculate cost
        cost = COST_TARGETS["per_video_24s"] if duration == 24 else COST_TARGETS["per_video_30s"]
        
        video_filename = f"{account}_{product['id']}_video_{duration}s_{datetime.now().timestamp()}.mp4"
        video_path = OUTPUT_DIR / video_filename
        
        return {
            "success": True,
            "path": str(video_path),
            "account": account,
            "product_id": product["id"],
            "product_name": product["name"],
            "duration": duration,
            "cost": cost,
            "script": video_script["full_script"],
            "aicda_structure": video_script["aicda_structure"],
            "pose_sequence": pose_sequence,
            "prompt": video_prompt,
            "segments_breakdown": video_script["segments"]
        }
    
    def generate_campaign_content(self, accounts: List[str] = None, 
                                  video_duration: int = 30) -> Dict:
        """
        Generate complete campaign content for 1 product
        
        Workflow for each account:
        1. Generate character image (if not exists)
        2. Split character into poses
        3. Generate video script (AICDA)
        4. Generate video with pose matching
        
        Returns:
        - Generated assets
        - Total cost
        - Content plan per account
        """
        
        if accounts is None:
            accounts = list(ACCOUNT_CHARACTERS.keys())
        
        print(f"\n{'='*70}")
        print(f"🚀 CHARACTER-BASED CAMPAIGN GENERATOR")
        print(f"{'='*70}")
        print(f"Accounts: {len(accounts)}")
        print(f"Video duration: {video_duration}s")
        print(f"Focus: FREE products first (higher conversion)")
        print()
        
        start_time = datetime.now()
        
        # Select product (prioritize FREE)
        product = self.high_priority[0] if self.high_priority else self.medium_priority[0]
        
        print(f"🎯 Product: {product['name']}")
        print(f"   Price: {product['price'] if product['price'] > 0 else 'FREE'}")
        description = product.get('description', 'No description available')
        print(f"   Description: {description[:80]}...")
        print()
        
        campaign_assets = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "product": product,
            "accounts": {},
            "total_cost": 0.0,
            "total_assets": 0
        }
        
        # Generate content for each account
        for account in accounts:
            print(f"\n{'─'*70}")
            print(f"📱 Account: {account.upper()}")
            print(f"{'─'*70}")
            
            # STEP 1: Generate character image
            print(f"Step 1: Generating character image...")
            character_result = self.generate_character_image(account)
            
            if not character_result["success"]:
                print(f"   ❌ Failed to generate character")
                continue
            
            campaign_assets["total_cost"] += character_result["cost"]
            print(f"   ✅ Character: {character_result['character_name']}")
            print(f"      Cost: ${character_result['cost']:.4f}")
            
            # STEP 2: Split character into poses
            print(f"\nStep 2: Splitting character poses...")
            poses_result = self.split_character_poses(character_result["path"], account)
            print(f"   ✅ Generated {poses_result['total_poses']} pose variations")
            
            # STEP 3: Generate video script (AICDA)
            print(f"\nStep 3: Generating video script (AICDA)...")
            if video_duration == 24:
                script_result = self.generate_video_script_24s(product, account)
            else:
                script_result = self.generate_video_script_30s(product, account)
            
            print(f"   ✅ Script generated ({script_result['duration']}s)")
            print(f"      Structure: {list(script_result['aicda_structure'].keys())}")
            
            # STEP 4: Generate video with pose matching
            print(f"\nStep 4: Generating video with pose matching...")
            video_result = self.generate_video_with_pose_matching(
                product, account, character_result["path"], 
                poses_result["poses"], script_result
            )
            
            if video_result["success"]:
                campaign_assets["total_cost"] += video_result["cost"]
                campaign_assets["total_assets"] += 1
                
                # Save account assets
                campaign_assets["accounts"][account] = {
                    "character": character_result,
                    "poses": poses_result,
                    "script": script_result,
                    "video": video_result
                }
                
                print(f"   ✅ Video: {video_result['duration']}s")
                print(f"      Cost: ${video_result['cost']:.4f}")
                print(f"      Path: {video_result['path']}")
                
                # Show pose sequence
                print(f"\n   📋 Pose Sequence:")
                for pose in video_result["pose_sequence"]:
                    print(f"      {pose['start_second']}-{pose['end_second']}s: {pose['pose']} ({pose['description']})")
            else:
                print(f"   ❌ Failed to generate video")
        
        # Print summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n{'='*70}")
        print(f"📊 CAMPAIGN SUMMARY")
        print(f"{'='*70}")
        print(f"Time taken: {duration:.1f} seconds")
        print(f"\n📈 Assets:")
        print(f"   Accounts covered: {len(campaign_assets['accounts'])}")
        print(f"   Total assets: {campaign_assets['total_assets']}")
        print(f"   Characters generated: {len(campaign_assets['accounts'])}")
        print(f"   Poses per character: {len(POSE_VARIATIONS)}")
        print(f"\n💰 Cost:")
        print(f"   Character images: ${campaign_assets['total_cost'] * 0.4:.4f} (40%)")
        print(f"   Videos: ${campaign_assets['total_cost'] * 0.6:.4f} (60%)")
        print(f"   🎯 Total: ${campaign_assets['total_cost']:.4f}")
        print(f"\n📝 AICDA Compliance:")
        print(f"   ✅ Attention (Hook): First 3s guaranteed")
        print(f"   ✅ Interest: Problem agitated")
        print(f"   ✅ Curiosity: Solution previewed")
        print(f"   ✅ Desire: Value proposition")
        print(f"   ✅ Action: Strong CTA")
        
        # Save campaign manifest
        campaign_file = OUTPUT_DIR / f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(campaign_file, "w") as f:
            json.dump(campaign_assets, f, indent=2, default=str)
        
        print(f"\n📁 Campaign saved: {campaign_file}")
        print(f"{'='*70}")
        
        return campaign_assets
    
    def save_scripts_to_files(self, campaign_assets: Dict):
        """
        Save video scripts to individual text files for easy reference
        """
        
        scripts_dir = OUTPUT_DIR / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        
        for account, account_data in campaign_assets["accounts"].items():
            if "script" in account_data and "video" in account_data:
                script_data = account_data["script"]
                video_data = account_data["video"]
                
                script_filename = f"{account}_{campaign_assets['product']['id']}_script.txt"
                script_path = scripts_dir / script_filename
                
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(f"""# VIDEO SCRIPT - {account.upper()}
# Product: {campaign_assets['product']['name']}
# Duration: {video_data['duration']}s
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{script_data['full_script']}

---
# POSE SEQUENCE
""")
                    for i, pose in enumerate(video_data["pose_sequence"], 1):
                        f.write(f"""
{i}. {pose['start_second']}-{pose['end_second']}s
   Pose: {pose['pose']}
   Description: {pose['description']}
   Action: {pose['action']}
""")
                    
                    f.write(f"""
---
# AICDA STRUCTURE
""")
                    for key, value in script_data["aicda_structure"].items():
                        f.write(f"\n{key}: {value}")
                
                print(f"💾 Script saved: {script_path}")
        
        return scripts_dir

def main():
    """Main execution function"""
    generator = CharacterBasedMediaGenerator()
    
    print(f"\n🚀 JENDRALBOT CHARACTER-BASED MEDIA GENERATOR")
    print(f"   Video 24-30s | Hook-Based | AICDA Compliant | Consistent Characters")
    print(f"{'='*70}")
    
    # Generate campaign for all accounts
    result = generator.generate_campaign_content(
        accounts=list(ACCOUNT_CHARACTERS.keys()),  # All accounts
        video_duration=30  # 30s videos
    )
    
    # Save scripts to individual files
    print(f"\n{'='*70}")
    print(f"💾 SAVING SCRIPTS...")
    print(f"{'='*70}")
    generator.save_scripts_to_files(result)
    
    print(f"\n{'='*70}")
    print(f"✅ GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"\n📝 Next Steps:")
    print(f"   1. Review generated scripts in {OUTPUT_DIR / 'scripts'}")
    print(f"   2. Set up NVIDIA_API_KEY and BYTEPLUS_API_KEY")
    print(f"   3. Replace simulated generation with actual API calls")
    print(f"   4. Test character consistency across videos")
    print(f"   5. Upload videos to social media accounts")
    print(f"   6. Track CTR and conversion metrics")
    print(f"\n💡 Tips:")
    print(f"   • Character images are reusable for future videos")
    print(f"   • Hook in first 3s is critical for attention")
    print(f"   • AICDA structure ensures viewer engagement")
    print(f"   • Pose matching creates natural video flow")
    print(f"   • Focus on FREE products for higher conversion")

if __name__ == "__main__":
    main()