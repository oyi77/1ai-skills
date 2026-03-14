#!/usr/bin/env python3
"""
High-Quality Text Image Generator for JENDRALBOT
Creates professional 4:5 vertical images with hooks
Dark background, white text, viral-ready
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

workspace = os.path.expanduser("~/.openclaw/workspace")

class TextImageGenerator:
    """Generate high-quality text-based images from hooks"""
    
    def __init__(self):
        print("\n🎨 Initializing High-Quality Text Image Generator...")
        
        # Configuration
        self.config = {
            "width": 1080,
            "height": 1350,
            "background": "#000000",  # Pure black
            "text_color": "#FFFFFF",  # Pure white
            "font_family": "Arial"
        }
        
        # Load hooks
        self.hooks_db_path = os.path.join(workspace, "hooks/jendralbot_complete.json")
        with open(self.hooks_db_path, 'r') as f:
            self.db = json.load(f)
        
        self.load_hooks()
        
        # Setup output directory
        self.output_dir = os.path.join(workspace, "generated_posts/images")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Try to load fonts
        self.fonts = self.load_fonts()
    
    def load_hooks(self):
        """Load all hooks"""
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
    
    def load_fonts(self):
        """Load fonts, use system defaults as fallback"""
        fonts = {}
        
        # Try to load fonts, use system defaults if not available
        try:
            fonts['headline'] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            fonts['body'] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            fonts['cta'] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", 24)
            fonts['watermark'] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            # Fallback to default fonts
            fonts['headline'] = ImageFont.load_default()
            fonts['body'] = ImageFont.load_default()
            fonts['cta'] = ImageFont.load_default()
            fonts['watermark'] = ImageFont.load_default()
        
        return fonts
    
    def create_image(self, hook):
        """
        Create high-quality image from hook
        
        Returns:
            PIL Image object
        """
        # Create black background
        img = Image.new('RGB', (self.config['width'], self.config['height']), color=self.config['background'])
        draw = ImageDraw.Draw(img)
        
        # Get text colors
        text_color = self.config['text_color']
        
        # Draw headline (top section)
        self.draw_text_centered(
            draw, 
            hook['headline'], 
            self.fonts['headline'], 
            self.config['width'] // 2, 
            200,  # Top margin
            text_color,
            max_width=900
        )
        
        # Draw body (middle section)
        self.draw_multiline_text_centered(
            draw,
            hook['body'],
            self.fonts['body'],
            self.config['width'] // 2,
            450,  # Starting Y position
            text_color,
            max_width=900,
            line_height=40
        )
        
        # Draw CTA (bottom section)
        self.draw_text_centered(
            draw,
            hook['cta'],
            self.fonts['cta'],
            self.config['width'] // 2,
            1050,  # Bottom section
            text_color,
            max_width=900
        )
        
        # Draw watermark (bottom right)
        self.draw_watermark(draw, "JENDRALBOT", 20)
        
        # Draw product tag (bottom left)
        self.draw_product_tag(draw, hook['product'], 20)
        
        return img
    
    def draw_text_centered(self, draw, text, font, x, y, color, max_width=None):
        """Draw single line text centered"""
        if max_width:
            text = self.wrap_text(text, font, max_width)[0]
        
        # Calculate text position for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        
        draw.text((x - text_width // 2, y), text, font=font, fill=color)
    
    def draw_multiline_text_centered(self, draw, text, font, x, y, color, max_width=None, line_height=None):
        """Draw multiline text centered"""
        lines = text.split('\n')
        
        current_y = y
        
        for line in lines:
            if max_width:
                wrapped_lines = self.wrap_text(line, font, max_width)
            else:
                wrapped_lines = [line]
            
            for wrapped_line in wrapped_lines:
                bbox = draw.textbbox((0, 0), wrapped_line, font=font)
                text_width = bbox[2] - bbox[0]
                
                draw.text((x - text_width // 2, current_y), wrapped_line, font=font, fill=color)
                current_y += self.fonts['body'].size if line_height is None else line_height
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            
            if bbox[2] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def draw_watermark(self, draw, text, margin):
        """Draw watermark in bottom right"""
        bbox = draw.textbbox((0, 0), text, font=self.fonts['watermark'])
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = self.config['width'] - text_width - margin
        y = self.config['height'] - text_height - margin
        
        draw.text((x, y), text, font=self.fonts['watermark'], fill="#666666")
    
    def draw_product_tag(self, draw, product_name, margin):
        """Draw product tag in bottom left"""
        bbox = draw.textbbox((0, 0), product_name, font=self.fonts['watermark'])
        text_height = bbox[3] - bbox[1]
        
        x = margin
        y = self.config['height'] - text_height - margin
        
        draw.text((x, y), product_name, font=self.fonts['watermark'], fill="#666666")
    
    def generate_all_images(self):
        """Generate images for all hooks"""
        print(f"\n🎨 Generating {len(self.all_hooks)} high-quality images...")
        
        count = 0
        
        for i, hook in enumerate(self.all_hooks):
            try:
                # Create image
                img = self.create_image(hook)
                
                # Save image
                filename = f"hook_{i:04d}_{hook['product'].replace(' ', '_')}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                img.save(filepath, "PNG", quality=95)
                
                count += 1
                
                if count % 20 == 0:
                    print(f"  Progress: {count}/{len(self.all_hooks)} images generated")
            
            except Exception as e:
                print(f"  ⚠️  Error generating image {i}: {str(e)}")
        
        print(f"\n✅ Generated {count} images")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📊 Image size: {self.config['width']}x{self.config['height']}px")
        print(f"🎨 Style: Dark background, white text, professional")
        
        return count

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='High-Quality Text Image Generator')
    parser.add_argument('--count', type=int, default=156, help='Number of images to generate')
    parser.add_argument('--test', action='store_true', help='Generate 1 test image')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = TextImageGenerator()
    
    if args.test:
        print("\n🧪 Generating 1 test image...")
        
        # Generate first hook as test
        hook = generator.all_hooks[0]
        img = generator.create_image(hook)
        
        test_path = os.path.join(output_dir, "test_image.png")
        img.save(test_path, "PNG", quality=95)
        
        print(f"✅ Test image saved: {test_path}")
    
    else:
        count = generator.generate_all_images()
        print(f"\n🎉 Complete! {count} images ready for posting")

if __name__ == "__main__":
    main()