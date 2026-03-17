#!/bin/bash

for video in /home/openclaw/.openclaw/workspace/output/trading_30days/day_*/post_[1-3]_final.mp4; do
  echo "Processing: $video"
  
  # Get upload URL
  upload_response=$(curl -s -X POST "https://api.post-bridge.com/v1/media/create-upload-url" \
    -H "Authorization: Bearer pb_live_AT9Xm4PKaYBzAvFZYGgexi" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$(basename "$video")\", \"mime_type\": \"video/mp4\", \"size_bytes\": 10000000}")
  
  media_id=$(echo "$upload_response" | jq -r '.media_id')
  upload_url=$(echo "$upload_response" | jq -r '.upload_url')
  
  if [ -z "$media_id" ] || [ -z "$upload_url" ]; then
    echo "❌ Failed to get upload URL for $video"
    continue
  fi
  
  # Upload file
  curl -T "$video" "$upload_url" || {
    echo "❌ Upload failed for $video"
    continue
  }
  
  # Determine day and post number for caption
  day=$(echo "$video" | grep -o 'day_[0-9]*' | cut -d'_' -f2)
  post_num=$(echo "$video" | grep -o 'post_[0-9]' | cut -d'_' -f2)
  
  # Create caption
  caption="🔥 Trading Day $day: #$post_num\n\nPart of 30-Day #TradingChallenge by @AlgoExpertHub\nFull strategy → https://lynk.id/jendralbot\n\n#XAUUSD #TradingEdu #ForexIndonesia"
  
  # Schedule post
  schedule_response=$(curl -s -X POST "https://api.post-bridge.com/v1/posts" \
    -H "Authorization: Bearer pb_live_AT9Xm4PKaYBzAvFZYGgexi" \
    -H "Content-Type: application/json" \
    -d "{\"caption\": \"${caption}\", \"social_accounts\": [49816, 49810, 49811, 49814], \"media\": [\"${media_id}\"], \"use_queue\": true}")
  
  post_id=$(echo "$schedule_response" | jq -r '.id')
  if [ -n "$post_id" ]; then
    echo "✅ Scheduled: $video → Post ID: $post_id"
  else
    echo "❌ Failed to schedule: $video → Response: $schedule_response"
  fi

done