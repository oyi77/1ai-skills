#!/usr/bin/env python3
"""
Remotion Animation Creator - Generate animation configs

Usage:
    python3 create_animation.py --template <template> --text <text> --duration <seconds>

Author: Vilona (BerkahKarya AI)
Date: 2026-03-17
"""

import json
import sys
import os
from pathlib import Path

# Output directory
OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "temp" / "remotion_animations"

# Template configurations
TEMPLATES = {
    "kinetic_typo": {
        "type": "kinetic_typo",
        "default_duration": 3,
        "params": {
            "text": {"required": True, "type": "str"},
            "animation": {"default": "scale-in", "options": ["scale-in", "word-by-word", "slide-up", "gradient-reveal", "typewriter"]},
            "duration": {"default": 3, "type": "int"},
            "fontSize": {"default": 80, "type": "int"},
            "fontWeight": {"default": 800, "type": "int"},
            "colors": {"default": ["#FF6B6B", "#4ECDC4"], "type": "list"}
        }
    },
    
    "product_showcase": {
        "type": "product_showcase",
        "default_duration": 8,
        "params": {
            "image": {"required": True, "type": "str"},
            "animation": {"default": "3d-rotate", "options": ["3d-rotate", "feature-highlight", "zoom-in", "splitscreen", "multi-angle"]},
            "rotation_degrees": {"default": 360, "type": "int"},
            "duration": {"default": 8, "type": "int"},
            "caption": {"default": "", "type": "str"}
        }
    },
    
    "data_viz": {
        "type": "data_viz",
        "default_duration": 5,
        "params": {
            "animation": {"default": "counter", "options": ["counter", "bar-chart-growth", "progress-bar", "pie-chart"]},
            "start": {"default": 0, "type": "int"},
            "end": {"required": True, "type": "int"},
            "duration": {"default": 5, "type": "int"},
            "format": {"default": "#,###", "type": "str"}
        }
    },
    
    "logo_reveal": {
        "type": "logo_reveal",
        "default_duration": 5,
        "params": {
            "image": {"required": True, "type": "str"},
            "animation": {"default": "path-draw", "options": ["path-draw", "scale-fade", "rotate-in", "glow-effect"]},
            "duration": {"default": 5, "type": "int"},
            "glow": {"default": False, "type": "bool"}
        }
    },
    
    "social_post": {
        "type": "social_post",
        "default_duration": 3,
        "params": {
            "platform": {"required": True, "options": ["tiktok", "reels", "youtube-shorts"]},
            "template": {"default": "tiktok-intro", "options": ["tiktok-intro", "reels-hook", "youtube-shorts"]},
            "text": {"required": True, "type": "str"},
            "duration": {"default": 3, "type": "int"}
        }
    }
}

def create_animation_config(template_name, params):
    """Create animation configuration JSON"""
    
    if template_name not in TEMPLATES:
        print(f"❌ Template '{template_name}' not found")
        print(f"Available templates: {', '.join(TEMPLATES.keys())}")
        return None
    
    template = TEMPLATES[template_name]
    config = {
        "type": template["type"],
        "template": template_name,
        "created_at": datetime.now().isoformat()
    }
    
    # Add parameters
    for param_name, param_config in template["params"].items():
        if param_name in params:
            config[param_name] = params[param_name]
        elif "default" in param_config:
            config[param_name] = param_config["default"]
    
    return config

def save_config(config, filename=None):
    """Save config to file"""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if filename is None:
        text_content = config.get("text", config.get("template", "animation"))
        filename = f"animation_{text_content[:20].replace(' ', '_')}.json"
    
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=2)
    
    return str(filepath)

def main():
    """Main entry point"""
    
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nAvailable templates:")
        for name, template in TEMPLATES.items():
            print(f"  • {name} - {template['type']}")
        sys.exit(1)
    
    # Parse arguments
    args = {}
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "--template" and i + 1 < len(sys.argv):
            args["template"] = sys.argv[i + 1]
            i += 2
        elif arg == "--text" and i + 1 < len(sys.argv):
            args["text"] = sys.argv[i + 1]
            i += 2
        elif arg == "--duration" and i + 1 < len(sys.argv):
            args["duration"] = int(sys.argv[i + 1])
            i += 2
        elif arg == "--output" and i + 1 < len(sys.argv):
            args["output"] = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    if "template" not in args:
        print("❌ --template is required")
        sys.exit(1)
    
    # Create config
    config = create_animation_config(args["template"], args)
    
    if config is None:
        sys.exit(1)
    
    # Save config
    output_file = save_config(config, args.get("output"))
    
    print("✅ Animation config created")
    print(f"   Template: {args['template']}")
    print(f"   Type: {config['type']}")
    print(f"   Output: {output_file}")
    print("\nNext steps:")
    print("   1. Create Remotion project: npx create-video@latest remotion-project")
    print(f"   2. Copy config: cp {output_file} remotion-project/")
    print("   3. Preview: npm run dev")
    print("   4. Render: npm run build")

if __name__ == "__main__":
    from datetime import datetime
    main()
