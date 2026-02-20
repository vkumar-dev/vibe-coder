# Vibe Coder Worker for Railway/Cloud Hosting
# This script runs the vibe coder daemon for cloud deployment

#!/usr/bin/env python3
"""
Vibe Coder - Cloud Worker

Runs vibe coder as a background worker for cloud platforms.
Use this for Railway, Render, Fly.io, etc.

Usage: python run_worker.py
"""

import asyncio
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vibe_coder import run_vibe_cycle


async def main():
    """Run vibe coder worker."""
    print("="*60)
    print("  🎨 Vibe Coder - Cloud Worker")
    print("="*60)
    print(f"  Started at: {datetime.utcnow().isoformat()}")
    print(f"  Interval: 4 hours")
    print("="*60)
    
    # Run initial cycle
    print("\n🚀 Running initial cycle...")
    await run_vibe_cycle(max_iterations=5)
    
    # Continue running cycles
    interval_hours = int(os.environ.get('VIBE_INTERVAL', '4'))
    
    while True:
        next_run = datetime.utcnow().timestamp() + (interval_hours * 3600)
        print(f"\n💤 Sleeping until {datetime.fromtimestamp(next_run).isoformat()}")
        print(f"   (Next cycle in {interval_hours} hours)")
        
        await asyncio.sleep(interval_hours * 3600)
        
        # Run next cycle
        print("\n🚀 Running next cycle...")
        try:
            await run_vibe_cycle(max_iterations=5)
        except Exception as e:
            print(f"❌ Cycle failed: {e}")
            print("   Continuing to next cycle...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Worker stopped")
        sys.exit(0)
