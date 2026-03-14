#!/usr/bin/env python3
"""
Visual Post Generator - Creates 4:5 vertical images from hooks
Dark background, white text, professional design
"""

import json
import os
from datetime import datetime
import subprocess

workspace = os.path.expanduser("~/.openclaw/workspace")

class VisualGenerator:
    """Generate visual posts from hooks"""
    
    def __init__(self):
        print(f"\n🎨 Initializing Visual Post Generator...")
        
        self.hooks_db_path = os.path.join(workspace, "hooks/jendralbot_complete.json")
        self.output_dir = os.path.join(workspace, "generated_posts/visuals")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.load_hooks()
    
    def load_hooks(self):
        """Load hooks from database"""
        with open(self.hooks_db_path, 'r') as f:
            self.db = json.load(f)
        
        self.all_hooks = []
        
        for product in self.db['products']:
            hooks_file = os.path.join(workspace, product['hooks_file'])
            
            if os.path.exists(hooks_file):
                with open(hooks_file, 'r') as f:
                    data = json.load(f)
                    for hook in data['hooks']:
                        hook['product'] = product['name']
                        hook['lynk'] = product['lynk']
                        self.all_hooks.append(hook)
        
        print(f"✅ Loaded {len(self.all_hooks)} hooks")
    
    def generate_visual_config(self, hook):
        """
        Generate visual configuration for a hook
        
        Returns:
            dict: Configuration for image generation
        """
        config = {
            "format": "4:5 vertical (1080x1350)",
            "background": {
                "color": "#000000",  # Black
                "style": "solid"
            },
            "text": {
                "color": "#FFFFFF",  # White
                "font_family": "Arial Black, Arial, sans-serif",
                "alignment": "center",
                "sections": [
                    {
                        "type": "headline",
                        "text": hook['headline'],
                        "font_size": "48px",
                        "font_weight": "bold",
                        "margin_top": "150px",
                        "margin_bottom": "50px"
                    },
                    {
                        "type": "body",
                        "text": hook['body'],
                        "font_size": "28px",
                        "font_weight": "normal",
                        "max_width": "800px",
                        "line_height": "1.5",
                        "margin_bottom": "50px"
                    },
                    {
                        "type": "cta",
                        "text": hook['cta'],
                        "font_size": "24px",
                        "font_weight": "normal",
                        "margin_bottom": "150px",
                        "style": "italic"
                    }
                ]
            },
            "branding": {
                "product": hook['product'],
                "lynk": hook['lynk'],
                "watermark": "JENDRALBOT",
                "position": "bottom-right"
            },
            "generated_at": datetime.now().isoformat()
        }
        
        return config
    
    def save_visual_config(self, config, hook_index):
        """Save visual configuration to file"""
        filename = f"visual_{hook_index:03d}_{config['branding']['product'].replace(' ', '_')}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        
        return filepath
    
    def generate_all_visuals(self):
        """Generate visual configurations for all hooks"""
        print(f"\n🎨 Generating visual configurations for {len(self.all_hooks)} hooks...")
        
        count = 0
        for i, hook in enumerate(self.all_hooks):
            config = self.generate_visual_config(hook)
            filepath = self.save_visual_config(config, i)
            count += 1
            print(f"  [{count}/{len(self.all_hooks)}] {filepath}")
        
        print(f"\n✅ Generated {count} visual configuration files")
        print(f"📁 Output directory: {self.output_dir}")
        
        return count
    
    def test_image_generation(self):
        """Test actual image generation (if nano-banana-pro available)"""
        print(f"\n🧪 Testing image generation...")
        
        # Generate one test visual
        if self.all_hooks:
            test_hook = self.all_hooks[0]
            config = self.generate_visual_config(test_hook)
            
            # Try nano-banana-pro skill
            nano_banana_path = os.path.join(workspace, "skills/nano-banana-pro")
            
            if os.path.exists(nano_banana_path):
                print(f"✅ nano-banana-pro skill found")
                
                # Create prompt from config
                prompt = f"Create 4:5 vertical image with these elements:\n"
                prompt += f"Background: Black\n"
                prompt += f"Headline (white, bold, 48px): {config['text']['sections'][0]['text']}\n"
                prompt += f"Body (white, 28px): {config['text']['sections'][1]['text']}\n"
                prompt += f"CTA (white, 24px, italic): {config['text']['sections'][2]['text']}\n"
                prompt += f"Watermark: JENDRALBOT"
                
                print(f"Prompt: {prompt}")
                
                # TODO: Execute nano-banana-pro skill here
                print(f"⏳ Image generation ready (needs nano-banana-pro integration)")
                
            else:
                print(f"❌ nano-banana-pro skill not found")
                print(f"⏳ Using alternative: Manual Figma/Canva or PIL generation")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Visual Post Generator')
    parser.add_argument('--generate', action='store_true', help='Generate all visual configs')
    parser.add_argument('--test', action='store_true', help='Test image generation')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = VisualGenerator()
    
    if args.generate:
        count = generator.generate_all_visuals()
        print(f"\n🎉 Complete! {count} visual configurations ready for posting")
    
    elif args.test:
        generator.test_image_generation()
    
    else:
        print("\nUse --generate to create visual configurations")
        print("Use --test to test image generation")
        parser.print_help()

if __name__ == "__main__":
    main()