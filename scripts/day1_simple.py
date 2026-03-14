#!/usr/bin/env python3
# Simple Day 1 Planner
import json
products = ['guru_pintar_ai', 'belanja_duit_balik']
schedule = {"date": "2026-03-07", "phase": "Foundation Day 1", "posts": []}

for hour in range(0, 24, 2):
    if hour % 4 == 0:
        product_key = products[0]
    else:
        product_key = products[1]
    
    # Alternate type every 2 hours: 00, 02, 04, 06... → Sales, Edu, Sales, Edu, Sales, Edu
    post_type = "education" if (hour // 2) % 2 == 1 else "sales"
    
    post = {
        "time": f"{hour:02d}:00",
        "type": post_type,
        "product": product_key,
        "caption": f"{product_key} post at {hour:02d}:00"
    }
    
    schedule["posts"].append(post)

# Save
with open("day1_simple_schedule.json", "w") as f:
    json.dump(schedule, f, indent=2)

print("=" * 80)
print("DAY 1 - START FROM ZERO")
print("=" * 80)
print(f"Date: {schedule['date']}")
print(f"Products: {products[0]} / {products[1]}")
print()
print("Time  | Type      | Product")
print("-" * 60)
for post in schedule["posts"]:
    icon = "💰" if post["type"] == "sales" else "📚"
    print(f"{post['time']} | {post['type'].upper():7s} | {post['product'][:20]}")

print()
print("=" * 80)
print("Total: 12 posts")
print("Sales: 6 (soft sells only 20%)")
print("Education: 6 (value-first 80%)")
print("=" * 80)
print("Saved: day1_simple_schedule.json")