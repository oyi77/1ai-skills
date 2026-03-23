#!/usr/bin/env python3
"""CLI wrapper to update LYNK text blocks using opencli.

Usage examples:
  python scripts/lynk_update_copy.py parenting hero
  python scripts/lynk_update_copy.py parenting social
  python scripts/lynk_update_copy.py parenting urgency

This assumes you have an opencli "lynk" command installed that exposes
  lynk update-text --product-id <ID> --block-id <BLOCK> --file <PATH>

to actually drive the browser.
"""

import argparse
import subprocess
from pathlib import Path

# Map logical product+section -> (product_id, block_id, template_path)
# TODO: fill real product_id and block_id from live LYNK once confirmed.
MAPPING = {
    ("parenting", "hero"): {
        "product_id": "69b9cfd8bd979855b5164dec-4215-2764687765-1773785048878",
        "block_id": "HEADER_FLASH_SALE",  # placeholder, replace with real block id
        "template": "templates/parenting_hero.html",
    },
    ("parenting", "social"): {
        "product_id": "69b9cfd8bd979855b5164dec-4215-2764687765-1773785048878",
        "block_id": "MIDDLE_SOCIAL_PROOF",  # placeholder
        "template": "templates/parenting_social_proof.html",
    },
    ("parenting", "urgency"): {
        "product_id": "69b9cfd8bd979855b5164dec-4215-2764687765-1773785048878",
        "block_id": "FOOTER_URGENCY",  # placeholder
        "template": "templates/parenting_urgency.html",
    },
}


def run_opencli(product: str, section: str) -> None:
    key = (product, section)
    cfg = MAPPING.get(key)
    if not cfg:
        raise SystemExit(f"No mapping configured for {product=}, {section=}")

    root = Path(__file__).resolve().parents[1]
    template_path = (root / cfg["template"]).resolve()
    if not template_path.is_file():
        raise SystemExit(f"Template not found: {template_path}")

    cmd = [
        "opencli",
        "lynk",
        "update-text",
        "--product-id",
        cfg["product_id"],
        "--block-id",
        cfg["block_id"],
        "--file",
        str(template_path),
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("product", help="logical product key, e.g. parenting")
    ap.add_argument("section", help="section key, e.g. hero|social|urgency")
    args = ap.parse_args()

    run_opencli(args.product, args.section)


if __name__ == "__main__":  # pragma: no cover
    main()
