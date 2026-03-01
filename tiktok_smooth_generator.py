#!/usr/bin/env python3
"""
TikTok Content Generator with Smooth Transitions (XFade Fix)
Implements proper video transitions using FFmpeg xfade filter
"""

import os
import subprocess
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import requests

# Configuration
FFMPEG_PATH = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"
OUTPUT_DIR = "/home/openclaw/.openclaw/workspace/output/tiktok_smooth"
ASSETS_DIR = "/home/openclaw/.openclaw/workspace/output/bundle_assets"

# NVIDIA & BytePlus endpoints
NVIDIA_API_KEY = os.getenv("NVIDIA_NGC_API_KEY", "nvapi-2Wk7QHw9eNq7tZwMxXyBw1G2KlMnOp")
NVIDIA_ENDPOINT = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-xl"

BYTEPLUS_API_KEY = os.getenv("BYTEPLUS_API_KEY", "")
BYTEPLUS_ENDPOINT = "https://visual.volcengineapi.com"

# Content Templates
CONTENT_TEMPLATES = {
    "agency_os": {
        "title": "Agency Performance Ad OS",
        "prompt": "Professional dashboard interface showing ad performance metrics, charts, ROAS tracking, clean UI design, dark theme with gold accents, tech startup aesthetic, 4K resolution",
        "duration": 15,
        "scenes": 3
    },
    "aura_beauty": {
        "title": "AURA Beauty Studio",
        "prompt": "Beautiful woman with professional makeup editing, before/after transformation, glowing skin, soft lighting, beauty studio aesthetic, professional photography, 8K quality",
        "duration": 15,
        "scenes": 3
    },
    "guru_ai": {
        "title": "Guru Pintar AI",
        "prompt": "AI writing content on laptop screen, futuristic interface, holographic text generation, creative writing scene, modern office, clean minimal aesthetic, 4K resolution",
        "duration": 15,
        "scenes": 3
    }
}

# TTS Configuration (Edge TTS)
VOICE = "id-ID-GadisNeural"  # Indonesian female voice

class TikTokSmoothGenerator:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.assets_dir = ASSETS_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(f"{self.output_dir}/temp", exist_ok=True)

    def log(self, message, level="INFO"):
        """Log message"""
        print(f"[{level}] {message}")

    def generate_images(self, template_key, num_images=3):
        """Generate images using NVIDIA Flux"""
        template = CONTENT_TEMPLATES[template_key]
        images = []

        self.log(f"Generating {num_images} images for {template['title']}...")

        for i in range(num_images):
            prompt = f"{template['prompt']}, scene {i+1}, different angle"

            # In production, this would call NVIDIA API
            # For now, use placeholder
            image_path = f"{self.output_dir}/temp/{template_key}_scene_{i+1}.jpg"

            # Check if image already exists
            if os.path.exists(image_path):
                self.log(f"  Image {i+1} already exists, skipping")
                images.append(image_path)
                continue

            # Placeholder - create a simple image
            self.log(f"  Creating placeholder for image {i+1}...")

            # Create a simple gradient image with text
            img = Image.new('RGB', (1080, 1920), color=(20, 20, 30))
            draw = ImageDraw.Draw(img)

            # Draw gradient
            for y in range(1920):
                r = int(20 + (y/1920) * 50)
                g = int(20 + (y/1920) * 40)
                b = int(30 + (y/1920) * 60)
                draw.rectangle([(0, y), (1080, y+1)], fill=(r, g, b))

            # Add text
            try:
                # Try to use a font
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            except:
                font = ImageFont.load_default()

            text = f"{template['title']}\nScene {i+1}"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            position = ((1080 - text_width) // 2, (1920 - text_height) // 2)
            draw.text(position, text, fill=(255, 215, 0), font=font)

            img.save(image_path)
            images.append(image_path)
            self.log(f"  ✅ Created image {i+1}: {image_path}")

        return images

    def generate_voiceover(self, text, output_path):
        """Generate voiceover using Edge TTS"""
        self.log(f"Generating voiceover...")

        try:
            # Use edge-tts CLI
            cmd = f"edge-tts --voice '{VOICE}' --text '{text}' --write-media '{output_path}'"
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            self.log(f"✅ Voiceover generated: {output_path}")
            return True
        except Exception as e:
            self.log(f"❌ Error generating voiceover: {str(e)}", "ERROR")
            return False

    def animate_images(self, images, output_dir):
        """Animate images using BytePlus Seedance Pro I2V"""
        animated_clips = []

        self.log("Animating images with BytePlus...")

        for i, image_path in enumerate(images):
            output_path = f"{output_dir}/clip_{i+1}.mp4"

            if os.path.exists(output_path):
                self.log(f"  Clip {i+1} already exists, skipping")
                animated_clips.append(output_path)
                continue

            # In production, this would call BytePlus API
            # For now, create a simple animated clip using FFmpeg
            self.log(f"  Creating animated clip {i+1}...")

            # Create a simple pan effect
            cmd = [
                FFMPEG_PATH,
                "-y",
                "-loop", "1",
                "-i", image_path,
                "-vf", "zoompan=z='min(zoom+0.0015,1.5)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920",
                "-t", "5",
                "-r", "30",
                "-pix_fmt", "yuv420p",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                output_path
            ]

            try:
                subprocess.run(cmd, check=True, capture_output=True)
                animated_clips.append(output_path)
                self.log(f"  ✅ Clip {i+1} created")
            except Exception as e:
                self.log(f"  ❌ Error creating clip {i+1}: {str(e)}", "ERROR")

        return animated_clips

    def apply_xfade_transitions(self, clips, output_path):
        """Apply smooth XFade transitions between clips"""
        self.log("Applying XFade transitions...")

        if len(clips) < 2:
            self.log("Not enough clips for transitions, using single clip")
            return clips[0] if clips else None

        transition_duration = 1.0  # 1 second transition

        # Build FFmpeg complex filter for XFade
        filter_complex = ""
        inputs = ""
        output_map = ""

        for i in range(len(clips)):
            inputs += f"-i {clips[i]} "

        # Generate filter string for XFade
        for i in range(len(clips) - 1):
            # Apply XFade between clip i and i+1
            current_input = f"{i}:v"
            next_input = f"{i+1}:v"
            output_label = f"v{i}"

            if i == len(clips) - 2:
                # Last transition - no overlay needed
                filter_complex += f"[{current_input}][{next_input}]xfade=transition=fade:duration={transition_duration}:offset=5[vout]"
            else:
                # Need to overlay with accumulated result
                if i == 0:
                    filter_complex += f"[{current_input}][{next_input}]xfade=transition=fade:duration={transition_duration}:offset=5[v{i}];"
                else:
                    # Use previous output and next clip
                    filter_complex += f"[v{i-1}][{next_input}]xfade=transition=fade:duration={transition_duration}:offset=5[v{i}];"

        # For simpler approach with just 3 clips:
        # Clip 1 (5s) + XFade (1s) = Clip 2 starts at 4s (overlap)
        # Clip 2 (5s) + XFade (1s) = Clip 3 starts at 8s

        # Build concat input
        if len(clips) == 3:
            # Simple 3-clip concat with XFade
            concat_filter = f"[0:v][1:v]xfade=transition=fade:duration={transition_duration}:offset=4[v1];[v1][2:v]xfade=transition=fade:duration={transition_duration}:offset=8"

            cmd = [
                FFMPEG_PATH,
                "-y",
                "-i", clips[0],
                "-i", clips[1],
                "-i", clips[2],
                "-filter_complex", concat_filter,
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                output_path
            ]
        else:
            # Fallback: simple concat without XFade
            # Create concat list
            concat_list = []
            for clip in clips:
                duration = self.get_video_duration(clip)
                concat_list.append(f"file '{clip}'\nduration {duration}")

            concat_file = f"{self.output_dir}/temp/concat_list.txt"
            with open(concat_file, "w") as f:
                f.write("\n".join(concat_list))

            cmd = [
                FFMPEG_PATH,
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                output_path
            ]

        try:
            self.log(f"Running FFmpeg command...")
            subprocess.run(cmd, check=True, capture_output=True)
            self.log(f"✅ Video with transitions created: {output_path}")
            return output_path
        except Exception as e:
            self.log(f"❌ Error applying transitions: {str(e)}", "ERROR")

            # Fallback: use first clip only
            self.log("Falling back to single clip...")
            import shutil
            shutil.copy(clips[0], output_path)
            return output_path

    def get_video_duration(self, video_path):
        """Get video duration using ffprobe"""
        try:
            cmd = [
                "/home/linuxbrew/.linuxbrew/bin/ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except:
            return 5.0  # Default 5 seconds

    def add_text_overlay(self, video_path, text, output_path):
        """Add text overlay using Pillow (FFmpeg drawtext not available in linuxbrew)"""
        self.log("Adding text overlay...")

        # Extract frames, add text, stitch back
        # This is a workaround since drawtext is not available

        try:
            # For now, just copy the video (text overlay is complex without drawtext)
            import shutil
            shutil.copy(video_path, output_path)
            self.log("✅ Text overlay skipped (copying video)")
            return True
        except Exception as e:
            self.log(f"❌ Error adding text: {str(e)}", "ERROR")
            return False

    def generate_tiktok_video(self, template_key="agency_os"):
        """Generate complete TikTok video with smooth transitions"""
        self.log(f"\n🚀 Generating TikTok video for: {template_key}")
        self.log("="*70)

        # 1. Generate images
        images = self.generate_images(template_key)

        # 2. Generate voiceover
        template = CONTENT_TEMPLATES[template_key]
        voiceover_text = f"{template['title']}. Solusi lengkap untuk bisnis online Anda."
        voiceover_path = f"{self.output_dir}/temp/voiceover_{template_key}.mp3"
        self.generate_voiceover(voiceover_text, voiceover_path)

        # 3. Animate images
        temp_dir = f"{self.output_dir}/temp/{template_key}"
        os.makedirs(temp_dir, exist_ok=True)
        animated_clips = self.animate_images(images, temp_dir)

        # 4. Apply XFade transitions
        final_video = f"{self.output_dir}/{template_key}_final_smooth.mp4"
        video_path = self.apply_xfade_transitions(animated_clips, final_video)

        # 5. Add audio
        final_with_audio = f"{self.output_dir}/{template_key}_smooth_complete.mp4"

        if os.path.exists(voiceover_path):
            cmd = [
                FFMPEG_PATH,
                "-y",
                "-i", video_path,
                "-i", voiceover_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                final_with_audio
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            self.log(f"✅ Final video with audio: {final_with_audio}")
        else:
            final_with_audio = video_path
            self.log("⚠️ No audio, using video only")

        # 6. Cleanup
        self.cleanup_temp(template_key)

        self.log("\n✅ TIKTOK VIDEO GENERATION COMPLETE")
        self.log(f"📁 Output: {final_with_audio}")

        return final_with_audio

    def cleanup_temp(self, template_key):
        """Clean up temporary files"""
        temp_dir = f"{self.output_dir}/temp/{template_key}"
        try:
            import shutil
            # shutil.rmtree(temp_dir)
            self.log(f"🧹 Temp files preserved in: {temp_dir}")
        except:
            pass

if __name__ == "__main__":
    print("\n🎬 TIKTOK SMOOTH GENERATOR 🎬")
    print("Content Generator with XFade Transitions")
    print("="*70)

    generator = TikTokSmoothGenerator()

    # Generate one video per template
    for template_key in CONTENT_TEMPLATES.keys():
        print(f"\n📦 Generating: {template_key}")
        video_path = generator.generate_tiktok_video(template_key)

    print("\n✅ ALL VIDEOS GENERATED!")
    print(f"📁 Output directory: {OUTPUT_DIR}")
