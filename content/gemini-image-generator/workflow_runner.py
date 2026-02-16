#!/usr/bin/env python3
"""
Workflow Runner for Gemini Image Generation
Full automation: Generate instruction → Process → Organize results.
"""

import argparse
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from prompt_optimizer import generate_instruction, generate_short_instruction

# Paths
WORKSPACE = Path(__file__).parent
INPUT_DIR = WORKSPACE / "input"
OUTPUT_DIR = WORKSPACE / "output"


def scan_input_folder(category: str = None) -> List[Path]:
    """Scan input folder for images to process"""
    images = []
    
    # Look for pose model images
    if category:
        category_dir = INPUT_DIR / category
        if category_dir.exists():
            images.extend(category_dir.glob("*.jpg"))
            images.extend(category_dir.glob("*.png"))
    else:
        images.extend(INPUT_DIR.glob("*.jpg"))
        images.extend(INPUT_DIR.glob("*.png"))
        
    return sorted(images)


def process_job(
    pose_image: Path,
    product_image: Optional[Path] = None,
    category: str = "fashion",
    product_name: str = "Product",
    style: str = None
) -> dict:
    """
    Process a single image generation job.
    
    Returns job details including the instruction.
    """
    job_id = f"gemini_{int(time.time())}_{pose_image.stem}"
    
    # Generate instruction
    instruction = generate_instruction(
        category=category,
        product_name=product_name,
        style=style
    )
    
    # Create job record
    job = {
        "id": job_id,
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "product": product_name,
        "pose_image": str(pose_image),
        "product_image": str(product_image) if product_image else None,
        "instruction": instruction,
        "status": "ready",
        "output_folder": str(OUTPUT_DIR / job_id)
    }
    
    # Save job file
    job_file = OUTPUT_DIR / f"{job_id}.json"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(job_file, 'w', encoding='utf-8') as f:
        json.dump(job, f, indent=2, ensure_ascii=False)
    
    return job


def print_job_summary(job: dict):
    """Print formatted job summary"""
    print("\n" + "="*70)
    print(f"JOB CREATED: {job['id']}")
    print("="*70)
    print(f"Category: {job['category']}")
    print(f"Product: {job['product']}")
    print(f"Pose Image: {job['pose_image']}")
    if job['product_image']:
        print(f"Product Image: {job['product_image']}")
    print("="*70)
    print("\nINSTRUCTION TO USE IN GEMINI:")
    print("-"*70)
    print(job['instruction'])
    print("-"*70)
    print("\nNext Steps:")
    print("1. Open Gemini: https://gemini.google.com/share/c7150b8213a4")
    print("2. Upload pose image")
    if job['product_image']:
        print("3. Upload product image")
    else:
        print("3. Upload product image (place in same visual)")
    print("4. Paste instruction above")
    print("5. Generate images")
    print("6. Download results to:", job['output_folder'])
    print("="*70)


def list_pending_jobs() -> List[dict]:
    """List all pending jobs"""
    jobs = []
    for job_file in OUTPUT_DIR.glob("gemini_*.json"):
        try:
            with open(job_file, 'r', encoding='utf-8') as f:
                job = json.load(f)
                if job.get('status') == 'ready':
                    jobs.append(job)
        except:
            continue
    return jobs


def batch_process(category: str = None):
    """Process all pending images in input folder"""
    images = scan_input_folder(category)
    
    if not images:
        print("No images found in ", INPUT_DIR)
        print("\nPlace images in:")
        if category:
            print(f"  {INPUT_DIR / category}")
        else:
            print(f"  {INPUT_DIR}")
        return
    
    print(f"\nFound {len(images)} images to process")
    
    # Group by category if possible
    for img in images:
        print(f"\nProcessing: {img.name}")
        # Simple heuristic: if image name contains category
        detected_category = category
        if not detected_category:
            for cat in ["fashion", "electronics", "food", "beauty", "home"]:
                if cat in img.name.lower():
                    detected_category = cat
                    break
            if not detected_category:
                detected_category = "fashion"  # default
        
        job = process_job(
            pose_image=img,
            category=detected_category,
            product_name=img.stem.replace("_", " ").title()
        )
        print_job_summary(job)


def main():
    parser = argparse.ArgumentParser(
        description="Gemini Image Generation Workflow Runner"
    )
    
    parser.add_argument(
        "--pose", "-p",
        type=Path,
        help="Path to pose model image"
    )
    
    parser.add_argument(
        "--product", "-pr",
        type=Path,
        help="Path to product image (optional)"
    )
    
    parser.add_argument(
        "--category", "-c",
        choices=["fashion", "electronics", "food", "beauty", "home"],
        default="fashion",
        help="Product category"
    )
    
    parser.add_argument(
        "--name", "-n",
        default="Product",
        help="Product name"
    )
    
    parser.add_argument(
        "--style", "-s",
        help="Visual style"
    )
    
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all images in input folder"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List pending jobs"
    )
    
    args = parser.parse_args()
    
    if args.list:
        jobs = list_pending_jobs()
        print(f"\nPending Jobs: {len(jobs)}")
        for job in jobs:
            print(f"  {job['id']}: {job['product']} ({job['category']})")
    
    elif args.batch:
        batch_process(args.category)
    
    elif args.pose:
        job = process_job(
            pose_image=args.pose,
            product_image=args.product,
            category=args.category,
            product_name=args.name,
            style=args.style
        )
        print_job_summary(job)
    
    else:
        print("Usage:")
        print("  Single image:")
        print("    python workflow_runner.py --pose model.jpg --product dress.jpg -c fashion -n 'Summer Dress'")
        print("\n  Batch process:")
        print("    python workflow_runner.py --batch -c fashion")
        print("\n  List pending:")
        print("    python workflow_runner.py --list")
        print(f"\nPlace images in: {INPUT_DIR}")


if __name__ == "__main__":
    main()
