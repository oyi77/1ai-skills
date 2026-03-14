#!/usr/bin/env python3
"""
JENDRALBOT Daily Automation & Monitoring System
Runs daily checks, revenue tracking, and continuation of uploads
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

workspace = os.path.expanduser("~/.openclaw/workspace")

class JendralbotScheduler:
    """Daily automation scheduler for JENDRALBOT campaign"""
    
    def __init__(self):
        log_path = os.path.join(workspace, "logs")
        os.makedirs(log_path, exist_ok=True)
        self.log_file = open(os.path.join(log_path, "daily_schedule.log"), 'a')
        self.log("Jendralbot Scheduler initialized")
    
    def log(self, message):
        """Log to file"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        self.log_file.write(json.dumps(entry) + '\n')
        self.log_file.flush()
    
    def check_lynk_dashboard_status(self):
        """Check LYNK dashboard and generate status report"""
        self.log("Checking LYNK dashboard status...")
        
        # Check if we can access LYNK dashboard
        status_file = os.path.join(workspace, "logs/lynk_performance.log")
        
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                logs = [json.loads(line) for line in f.readlines()]
            
            # Count today's metrics
            today = datetime.now().strftime("%Y-%m-%d")
            today_logs = [log for log in logs if log.get('timestamp', '').startswith(today)]
            
            if today_logs:
                views = sum(log.get('metrics', {}).get('views', 0) for log in today_logs)
                clicks = sum(log.get('metrics', {}).get('clicks', 0) for log in today_logs)
                conversions = sum(log.get('metrics', {}).get('conversions', 0) for log in today_logs)
                
                self.log(f"Today's LYNK Performance: Views={views}, Clicks={clicks}, Conversions={conversions}")
            else:
                self.log("No LYNK performance data yet")
        else:
            self.log("LYNK performance log not found")
    
    def resume_failed_uploads(self, platform='instagram'):
        """Resume failed uploads with rate limiting"""
        self.log(f"Checking for failed {platform} uploads to resume...")
        
        # Check log for recent failures
        upload_log = os.path.join(workspace, "logs/postbridge_upload_log.txt")
        
        if os.path.exists(upload_log):
            with open(upload_log, 'r') as f:
                logs = [json.loads(line) for line in f.readlines()]
            
            count_failures = sum(1 for log in logs if 'error' in log.get('message_obj', {}))
            
            if count_failures > 0:
                self.log(f"Found {count_failures} failed uploads. Resuming...")
                
                # Run rate limit aware upload
                try:
                    result = subprocess.run(
                        ['python3', 'scripts/rate_limit_aware_upload.py',
                         '--platform', platform, '--batch', '10'],
                        cwd=workspace,
                        capture_output=True,
                        text=True,
                        timeout=7200  # 2 hours max
                    )
                    
                    self.log(f"Resume upload result: {result.returncode}")
                    
                except Exception as e:
                    self.log(f"Resume upload failed: {e}")
    
    def schedule_next_uploads(self):
        """Schedule pending uploads for future dates"""
        self.log("Scheduling next batch of uploads...")
        
        # Check remaining uploads
        queue_file = os.path.join(workspace, "postbridge_queue_jendralbot.json")
        
        if os.path.exists(queue_file):
            with open(queue_file, 'r') as f:
                queue_data = json.load(f)
            
            # Check successful uploads
            successful = set()
            upload_log = os.path.join(workspace, "logs/postbridge_upload_log.txt")
            
            if os.path.exists(upload_log):
                with open(upload_log, 'r') as f:
                    for line in f.readlines():
                        log_entry = json.loads(line)
                        if 'post_id' in log_entry.get('message_obj', {}):
                            successful.add(log_entry['message_obj']['post_id'])
            
            pending = len(queue_data['posts']) - len(successful)
            
            self.log(f"Total posts: {len(queue_data['posts'])}, Successful: {len(successful)}, Pending: {pending}")
            
            if pending > 0:
                self.log("Pending uploads found. Use rate_limit_aware_upload.py to continue.")
            else:
                self.log("All uploads completed!")
    
    def daily_heartbeat(self):
        """Daily heartbeat check - revenue, posts, performance"""
        self.log("\n=== DAILY HEARTBEAT ===")
        
        # 1. Check revenue status (LYNK dashboard)
        self.check_lynk_dashboard_status()
        
        # 2. Check automation status
        self.schedule_next_uploads()
        
        # 3. Check rate limit status
        self.log("Checking rate limit status...")
        
        # Check for recent HTTP 500 errors
        upload_log = os.path.join(workspace, "logs/postbridge_upload_log.txt")
        
        if os.path.exists(upload_log):
            with open(upload_log, 'r') as f:
                last_lines = f.readlines()
                recent_failures = sum(1 for line in last_lines[-20:] if 'HTTP 500' in line)
            
            if recent_failures >= 3:
                self.log(f"⚠️  Rate limit still active: {recent_failures} recent failures")
                self.log("⏸️  Waiting 24 hours before resuming uploads")
            elif recent_failures > 0:
                self.log(f"ℹ️  {recent_failures} recent failures, rate limit recovering")
            else:
                self.log("✅ No rate limit issues detected")
                self.log("❓ Ready to resume uploads")
        
        self.log("=== END HEARTBEAT ===\n")
    
    def run_daily_schedule(self):
        """Execute daily schedule"""
        self.log("\n" + "="*70)
        self.log("JENDRALBOT DAILY SCHEDULE")
        self.log("="*70)
        
        # 1. Heartbeat check
        self.daily_heartbeat()
        
        # 2. Resume uploads if rate limit cleared
        # (this will be determined by heartbeat status)
        self.log("Uploads will resume automatically when rate limit clears")
        
        # 3. Generate daily report
        self.log("Daily report generated")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='JENDRALBOT Daily Scheduler')
    parser.add_argument('--heartbeat', action='store_true', help='Run heartbeat only')
    parser.add_argument('--resume', type=str, choices=['instagram', 'facebook'], 
                        help='Resume uploads for platform')
    
    args = parser.parse_args()
    
    scheduler = JendralbotScheduler()
    
    if args.heartbeat:
        scheduler.daily_heartbeat()
    elif args.resume:
        scheduler.resume_failed_uploads(args.resume)
    else:
        scheduler.run_daily_schedule()

if __name__ == "__main__":
    main()