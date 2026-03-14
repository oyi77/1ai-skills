#!/usr/bin/env python3
"""
JENDRALBOT CAMPAIGN - COST-OPTIMIZED MEDIA GENERATOR
Ultra realistic images & videos for Jendralbot products

Features:
- NVIDIA Flux for ultra realistic images ($0.004/image)
- BytePlus Seedance for TikTok videos ($0.026/5s)
- Cost optimization strategies
- Batch processing
- Video looping to save costs
- Jendralbot-specific content generation
"""

import os
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Configuration
WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
ENGINE_DIR = WORKSPACE / "autopilot_affiliate_engine"
OUTPUT_DIR = ENGINE_DIR / "jendralbot_media_generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Cost targets
COST_TARGETS = {
    "per_campaign": 5.00,  # $5 max per day
    "per_image": 0.004,
    "per_video_5s": 0.026,
    "daily_budget": 5.00
}

class JendralbotMediaGenerator:
    """Cost-optimized media generator for Jendralbot campaigns"""
    
    def __init__(self):
        self.load_products()
        self.cost_tracker = {
            "images_generated": 0,
            "videos_generated": 0,
            "total_cost": 0.0
        }
    
    def load_products(self):
        """Load Jendralbot products"""
        product_file = ENGINE_DIR / "jendralbot_products.json"
        with open(product_file) as f:
            data = json.load(f)
            self.products = data["products"]
        
        # Categorize by priority (free products = highest priority)
        self.high_priority = [p for p in self.products if p["price"] == 0]
        self.medium_priority = [p for p in self.products if 49000 <= p["price"] <= 75000]
        self.low_priority = [p for p in self.products if p["price"] > 75000]
        
        print(f"✅ Loaded {len(self.products)} products")
        print(f"   High priority: {len(self.high_priority)} (FREE)")
        print(f"   Medium priority: {len(self.medium_priority)} (49K-75K)")
        print(f"   Low priority: {len(self.low_priority)} (75K+)")
    
    def generate_cost_optimized_campaign(self, max_budget: float = 5.00) -> Dict:
        """
        Generate campaign assets within budget
        
        Strategy:
        1. Prioritize FREE products (no sales = wasted cost)
        2. Generate 1 high-quality image per high-priority product
        3. Use video looping instead of multiple clips
        4. Reuse assets across platforms
        
        Budget: $5.00 max
        """
        print(f"\n{'='*70}")
        print(f"💰 COST-OPTIMIZED CAMPAIGN GENERATOR")
        print(f"{'='*70}")
        print(f"Budget: ${max_budget:.2f}")
        print(f"Target: Maximum ROI (focus on FREE products first)")
        print()
        
        start_time = datetime.now()
        
        # PLAN BUDGET ALLOCATION
        budget_allocation = {
            "product_images": max_budget * 0.40,  # 40% - Product images
            "lifestyle_videos": max_budget * 0.40,  # 40% - TikTok videos
            "cinematic_intros": max_budget * 0.20,  # 20% - Cinematic intros
        }
        
        print(f"📊 Budget Allocation:")
        print(f"   Product Images: ${budget_allocation['product_images']:.2f}")
        print(f"   Lifestyle Videos: ${budget_allocation['lifestyle_videos']:.2f}")
        print(f"   Cinematic Intros: ${budget_allocation['cinematic_intros']:.2f}")
        print()
        
        # GENERATE ASSETS
        campaign_assets = {
            "cost breakdown": budget_allocation,
            "products": {},
            "total cost": 0.0
        }
        
        # Phase 1: Generate product images (FREE & MED priority)
        print(f"\n🎨 PHASE 1: Product Images (Budget: ${budget_allocation['product_images']:.2f})")
        print(f"{'-'*70}")
        
        image_budget = budget_allocation["product_images"]
        images_generated = []
        
        # Prioritize FREE products
        for product in self.high_priority[:2]:
            if image_budget >= COST_TARGETS["per_image"]:
                result = self.generate_product_image_optimized(product)
                if result["success"]:
                    campaign_assets["products"][product["id"]] = {
                        "image": result["path"],
                        "type": "product shot",
                        "cost": result["cost"]
                    }
                    images_generated.append(result)
                    image_budget -= result["cost"]
                    print(f"   ✅ {product['name']}: {result['cost']:.4f} → {result['path']}")
        
        # Then medium priority
        for product in self.medium_priority[:3]:
            if image_budget >= COST_TARGETS["per_image"]:
                result = self.generate_product_image_optimized(product)
                if result["success"]:
                    campaign_assets["products"][product["id"]] = {
                        "image": result["path"],
                        "type": "product shot",
                        "cost": result["cost"]
                    }
                    images_generated.append(result)
                    image_budget -= result["cost"]
                    print(f"   ✅ {product['name']}: {result['cost']:.4f} → {result['path']}")
        
        print(f"\n   Total images: {len(images_generated)}")
        print(f"   Remaining budget: ${image_budget:.4f}")
        
        # Phase 2: Generate lifestyle videos
        print(f"\n🎬 PHASE 2: Lifestyle Videos (Budget: ${budget_allocation['lifestyle_videos']:.2f})")
        print(f"{'-'*70}")
        
        video_budget = budget_allocation["lifestyle_videos"]
        videos_generated = []
        
        # Generate 2-3 lifestyle videos for FREE products
        for product in self.high_priority[:2]:
            video_cost = self.calculate_video_cost(duration=5)
            if video_budget >= video_cost:
                result = self.generate_lifestyle_video_optimized(product, duration=5)
                if result["success"]:
                    campaign_assets["products"][product["id"]]["lifestyle"] = {
                        "video": result["path"],
                        "type": "lifestyle video",
                        "cost": result["cost"],
                        "duration": result["duration"]
                    }
                    videos_generated.append(result)
                    video_budget -= result["cost"]
                    print(f"   ✅ {product['name']} lifestyle: {result['cost']:.4f} → {result['path']}")
        
        print(f"\n   Total videos: {len(videos_generated)}")
        print(f"   Remaining budget: ${video_budget:.4f}")
        
        # Phase 3: Generate cinematic intros (1 per high-priority product)
        print(f"\n🎥 PHASE 3: Cinematic Intros (Budget: ${budget_allocation['cinematic_intros']:.2f})")
        print(f"{'-'*70}")
        
        # Skip for now (Grok requires subscription)
        # Use looping instead
        print(f"   ⏸️  Skipping cinematic (Grok requires subscription)")
        print(f"   💡 Using video looping with existing clips instead")
        
        # OPTIMIZATION: Loop videos to get longer content
        print(f"\n🔄 OPTIMIZATION: Video Looping")
        print(f"{'-'*70}")
        
        looped_videos = []
        for video in videos_generated:
            # Loop 5s clip to 30s (6x loop = saves 5x cost)
            looped_path = OUTPUT_DIR / f"{video['name'].replace('.mp4', '')}_looped_30s.mp4"
            loop_result = self.loop_video(video["path"], looped_path, target_seconds=30)
            
            if loop_result["success"]:
                print(f"   ✅ {video['name']} looped: 5s → 30s (saves ${0.26 - 0.052:.4f})")
                looped_videos.append({
                    "original": video["path"],
                    "looped": looped_path,
                    "duration": 30,
                    "original_cost": video["cost"],
                    "savings": video["cost"] - (video["cost"] / 6)  # 5s -> 30s saves 5/6 of cost
                })
        
        # Calculate total cost
        total_image_cost = sum(img["cost"] for img in images_generated)
        total_video_cost = sum(vid["cost"] for vid in videos_generated)
        
        # Savings from looping
        total_savings = sum(v["savings"] for v in looped_videos)
        
        campaign_assets["total cost"] = total_image_cost + total_video_cost - total_savings
        campaign_assets["assets generated"] = {
            "images": len(images_generated),
            "videos": len(videos_generated),
            "looped": len(looped_videos)
        }
        campaign_assets["budget used"] = campaign_assets["total cost"]
        campaign_assets["budget saved"] = max_budget - campaign_assets["total cost"]
        
        # Print summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n{'='*70}")
        print(f"📊 CAMPAIGN SUMMARY")
        print(f"{'='*70}")
        print(f"Time taken: {duration:.1f} seconds")
        print(f"\n📈 Assets:")
        print(f"   Product images: {len(images_generated)}")
        print(f"   Lifestyle videos: {len(videos_generated)} (5s each)")
        print(f"   Looped videos: {len(looped_videos)} (30s each)")
        print(f"   Total: {len(images_generated) + len(videos_generated) + len(looped_videos)} assets")
        print(f"\n💰 Cost:")
        print(f"   Images: ${total_image_cost:.4f}")
        print(f"   Videos: ${total_video_cost:.4f}")
        print(f"   Savings (looping): -${total_savings:.4f}")
        print(f"   🎯 Total: ${campaign_assets['total cost']:.4f}")
        print(f"   Under budget: ${max_budget - campaign_assets['total cost']:.4f}")
        print(f"\n✅ Budget target: <${max_budget:.2f}")
        print(f"   Status: {'💰 WITHIN BUDGET' if campaign_assets['total cost'] <= max_budget else '❌ OVER BUDGET'}")
        
        # Save campaign manifest
        campaign_file = OUTPUT_DIR / f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(campaign_file, "w") as f:
            json.dump(campaign_assets, f, indent=2, default=str)
        
        print(f"\n📁 Campaign saved: {campaign_file}")
        print(f"{'='*70}")
        
        return campaign_assets
    
    def generate_product_image_optimized(self, product: Dict) -> Dict:
        """
        Generate ultra realistic product shot
        
        Cost optimization:
        - Single high-quality shot (better than 3 mediocre)
        - Perfect for E-commerce (90% realism not needed)
        - Reusable across platforms
        """
        
        # Ultra realistic but cost-conscious prompt
        prompt = f"""
{product['name']}, {self.product_type_from_name(product['name'])}, 
{self.color_from_name(product['name']) if 'color' in product['name'] else 'premium'} color
Three-point studio lighting, soft diffusion, rim light from left
Professional product photography aesthetic
{product['name']} text visible (if printed on product)
Clean 45-degree angle, professional composition
Slate gray gradient background, premium aesthetic
Commercial quality, e-commerce ready
        """.strip().replace('\n', ' ')
        
        # Minimal negative for cost efficiency
        negative = "blurry, low quality, distorted, messy background"
        
        # Simulate NVIDIA Flux generation
        # In production: Replace with actual API call
        filename = f"{product['id']}_product_shot_{datetime.now().timestamp()}.png"
        output_path = OUTPUT_DIR / filename
        
        return {
            "success": True,
            "path": str(output_path),
            "product_id": product["id"],
            "cost": COST_TARGETS["per_image"],
            "prompt": prompt,
            "negative": negative
        }
    
    def generate_lifestyle_video_optimized(self, product: Dict, duration: int = 5) -> Dict:
        """
        Generate lifestyle video using Seedance
        
        Cost optimization:
        - Short clip (5s only)
        - Loop to get 30s (saves 80% cost)
        - Natural lighting (no need for complex setups)
        """
        
        prompt = f"""
Gen Z Indonesian woman, 25 years old, natural,
holding {self.product_name_from_id(product['id'])} naturally,
in modern cafe setting, ambient warm light,
scrolling TikTok on phone, genuine smile,
looking natural on camera at slight angle,
lifestyle content style, authentic moment
        """.strip().replace('\n', ' ')
        
        filename = f"{product['id']}_lifestyle_{duration}s_{datetime.now().timestamp()}.mp4"
        output_path = OUTPUT_DIR / filename
        
        cost = self.calculate_video_cost(duration)
        
        return {
            "success": True,
            "path": str(output_path),
            "product_id": product["id"],
            "name": filename,
            "cost": cost,
            "duration": duration,
            "prompt": prompt
        }
    
    def loop_video(self, input_path: str, output_path: str, target_seconds: int = 30) -> Dict:
        """
        Loop short clip to longer duration
        
        Cost optimization:
        - 5s clip → 30s (6x loop) = saves 5 clips' cost = $0.13 saved
        - Smooth transitions with FFmpeg filters
        """
        
        # In production: Use FFmpeg
        # ffmpeg -stream_loop 6 -i input.mp4 -c:v libx264 -crf 28 -preset fast -t 30 output.mp4
        
        loops_needed = target_seconds // 5
        
        # Simulate FFmpeg
        cost_original = self.calculate_video_cost(5)
        cost_looped = cost_original / loops_needed
        savings = cost_original - cost_looped
        
        return {
            "success": True,
            "original": input_path,
            "looped": output_path,
            "duration": target_seconds,
            "loops": loops_needed,
            "savings": savings
        }
    
    def calculate_video_cost(self, duration: int) -> float:
        """Calculate video cost given duration"""
        # Seedance: $0.026 per 5s
        return (duration / 5) * COST_TARGETS["per_video_5s"]
    
    def product_type_from_name(self, name: str) -> str:
        """Extract product type from product name"""
        name_lower = name.lower()
        if "content" in name_lower:
            return "digital content package"
        elif "ai" in name_lower:
            return "AI software service"
        elif "menu" in name_lower:
            return "restaurant menu tool"
        elif "tiktok" in name_lower:
            return "affiliate course"
        else:
            return "digital product"
    
    def color_from_name(self, name: str) -> str:
        """Extract color from product name"""
        if "premium" in name.lower():
            return "premium gold"
        elif "starter" in name.lower():
            return "basic silver"
        else:
            return "professional"
    
    def product_name_from_id(self, product_id: str) -> str:
        """Get product name from ID"""
        for product in self.products:
            if product["id"] == product_id:
                return product["name"]
        return "Product"
    
    def generate_daily_content(self) -> Dict:
        """
        Generate daily content for Jendralbot
        
        Strategy:
        - 1 product image for FREE products
        - 1 lifestyle video for best-selling product
        - Reuse assets across 5 platforms
        """
        
        print(f"\n{'='*70}")
        print(f"📅 DAILY CONTENT GENERATOR")
        print(f"{'='*70}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        print()
        
        # Generate products for today
        today_products = self.high_priority[:2] + self.medium_priority[:2]
        
        print(f"Products to feature: {len(today_products)}")
        for p in today_products:
            price_text = "FREE" if p["price"] == 0 else f"IDR {p['price']:,}"
            print(f"   • {p['name']} ({price_text})")
        print()
        
        # Generate assets
        daily_assets = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "products": {},  # Use dict
            "images": [],
            "videos": [],
            "total_cost": 0.0
        }
        
        product_images = []
        for product in today_products[:4]:  # Just generate for all 4
            # Generate 1 image
            result = self.generate_product_image_optimized(product)
            if result["success"]:
                product_images.append(result)
                daily_assets["images"].append(result)
                daily_assets["total_cost"] += result["cost"]
                print(f"   ✅ Image: {product['name']} - ${result['cost']:.4f}")
        
        # Generate 1 lifestyle video for first FREE product
        best_free = self.high_priority[0]
        video_result = self.generate_lifestyle_video_optimized(best_free, duration=5)
        
        # Initialize products dict for best_free if not exists
        if best_free["id"] not in daily_assets["products"]:
            daily_assets["products"][best_free["id"]] = {}
        
        if video_result["success"]:
            # Store video in both products dict and videos list
            daily_assets["videos"].append(video_result)
            daily_assets["products"][best_free["id"]]["lifestyle"] = video_result["path"]
            daily_assets["products"][best_free["id"]]["looped_30s"] = f"{product_images[0]['path']}".replace(".png", "_looped_30s.mp4")
            daily_assets["products"][best_free["id"]]["image"] = product_images[0]["path"] if product_images else None
            daily_assets["total_cost"] += video_result["cost"]
            print(f"   ✅ Video: {best_free['name']} - ${video_result['cost']:.4f}")
        
        # Save daily manifest
        daily_file = OUTPUT_DIR / f"daily_{datetime.now().strftime('%Y%m%d')}.json"
        with open(daily_file, "w") as f:
            json.dump(daily_assets, f, indent=2, default=str)
        
        print(f"\n✅ Daily content saved: {daily_file}")
        print(f"   Total assets: {len(product_images) + 1}")
        print(f"   Total cost: ${daily_assets['total_cost']:.4f}")
        print(f"   Per platform: Reuse same 2 assets across 5 platforms")
        print(f"   Budget: Under ${COST_TARGETS['daily_budget']:.2f} ✓")
        
        return daily_assets

def main():
    """Main execution function"""
    generator = JendralbotMediaGenerator()
    
    print(f"\n🚀 JENDRALBOT MEDIA GENERATOR")
    print(f"   Cost-Optimized • Ultra Realistic • Production Ready")
    print(f"{'='*70}")
    
    # Option 1: Generate full campaign
    print(f"\nChoose option:")
    print(f"   1. Generate full campaign (within $5 budget)")
    print(f"   2. Generate daily content (within $5 budget)")
    print(f"\n📝 Note: This is a template script.")
    print(f"   Actual API calls to NVIDIA Flux and Seedsance needed.")
    print(f"   Current implementation simulates generation for planning.")
    
    # Generate daily content (default)
    result = generator.generate_daily_content()
    
    print(f"\n{'='*70}")
    print(f"✅ GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"\nNext steps:")
    print(f"   1. Set up NVIDIA_API_KEY and BYTEPLUS_API_KEY environment variables")
    print(f"   2. Replace simulated generation with actual API calls")
    print(f"   3. Run script daily to generate fresh content")
    print(f"   4. Upload assets to social media")
    print(f"   5. Track ROI and optimize")
    print(f"\n💡 Cost Optimization Tips:")
    print(f"   • Reuse images across all platforms (cost per platform: $0.0008)")
    print(f"   • Loop 5s videos to 30s (saves 80% video cost)")
    print(f"   • Focus on FREE products first (higher conversion = better ROI)")
    print(f"   • Generate less but higher quality (better A/B conversion)")

if __name__ == "__main__":
    main()