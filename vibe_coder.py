#!/usr/bin/env python3
"""
Vibe Coder - Main Entry Point

Autonomous app factory that ships 6 products per day.
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Optional

# Add current directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.research import ResearchAgent
from core.duplicate_checker import DuplicateChecker
from core.generator import AppGenerator, AppGenerationResult


def load_config() -> dict:
    """Load configuration."""
    import yaml
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


async def run_vibe_cycle(max_iterations: int = 1) -> dict:
    """Run a single vibe coding cycle."""
    print("\n" + "="*60)
    print("  🎨 VIBE CODER - Autonomous App Factory")
    print("="*60)
    print(f"  Starting cycle at {datetime.utcnow().isoformat()}")
    print("="*60)
    
    config = load_config()
    
    # Initialize components
    research_agent = ResearchAgent()
    duplicate_checker = DuplicateChecker(
        github_user=config.get('duplicate_check', {}).get('github_user', 'vkumar-dev')
    )
    generator = AppGenerator(config)
    
    results = {
        'cycle_start': datetime.utcnow().isoformat(),
        'ideas_processed': 0,
        'apps_generated': 0,
        'duplicates_skipped': 0,
        'apps': []
    }
    
    # Phase 1: Research
    print("\n" + "="*60)
    print("  Phase 1: Research")
    print("="*60)
    
    research_result = research_agent.run_full_research()
    
    # Get generated ideas
    ideas = research_agent.ideas
    
    if not ideas:
        print("⚠️  No ideas generated from research")
        return results
    
    # Phase 2: Check duplicates and generate apps
    print("\n" + "="*60)
    print("  Phase 2: Duplicate Check & Generation")
    print("="*60)
    
    apps_generated = 0
    
    for idea in ideas[:max_iterations]:
        results['ideas_processed'] += 1
        
        print(f"\n📋 Processing idea: {idea.title[:50]}...")
        
        # Check for duplicates
        duplicate_check = duplicate_checker.check_duplicate(
            idea_id=idea.id,
            idea_title=idea.title,
            idea_description=idea.description
        )
        
        if duplicate_check.is_duplicate:
            print(f"⚠️  Skipping duplicate idea")
            results['duplicates_skipped'] += 1
            continue
        
        # Generate app
        gen_result = generator.generate_app(
            idea_title=idea.title,
            idea_description=idea.description,
            idea_features=idea.features,
            idea_id=idea.id,
            is_ai_infused=idea.is_ai_infused,
            ai_capabilities=idea.ai_capabilities
        )
        
        results['apps'].append({
            'idea_id': idea.id,
            'app_name': gen_result.app_name,
            'success': gen_result.success,
            'github_repo': gen_result.github_repo,
            'error': gen_result.error
        })
        
        if gen_result.success:
            apps_generated += 1
            results['apps_generated'] += 1
            print(f"✅ App generated: {gen_result.app_name}")
            
            # Only generate 1 app per cycle (as per requirement)
            if apps_generated >= 1:
                print(f"\n🎯 Generated 1 app this cycle (limit reached)")
                break
        else:
            print(f"❌ App generation failed: {gen_result.error}")
    
    # Summary
    results['cycle_end'] = datetime.utcnow().isoformat()
    results['duration_seconds'] = (
        datetime.fromisoformat(results['cycle_end']) - 
        datetime.fromisoformat(results['cycle_start'])
    ).total_seconds()
    
    print("\n" + "="*60)
    print("  Cycle Complete")
    print("="*60)
    print(f"  Ideas processed: {results['ideas_processed']}")
    print(f"  Apps generated: {results['apps_generated']}")
    print(f"  Duplicates skipped: {results['duplicates_skipped']}")
    print(f"  Duration: {results['duration_seconds']:.1f}s")
    print("="*60)
    
    # Save cycle result
    save_cycle_result(results)
    
    return results


def save_cycle_result(results: dict):
    """Save cycle result to history."""
    history_file = os.path.join(os.path.dirname(__file__), 'state', 'history.json')
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    
    # Load existing history
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
        except Exception:
            history = []
    
    # Add new result
    history.append(results)
    
    # Save (keep last 100 cycles)
    with open(history_file, 'w') as f:
        json.dump(history[-100:], f, indent=2)


async def run_daemon(interval_hours: float = 4.0):
    """Run vibe coder as daemon (continuous)."""
    print("\n" + "="*60)
    print("  🎨 VIBE CODER - Daemon Mode")
    print("="*60)
    print(f"  Interval: {interval_hours} hours")
    print(f"  Apps per day: {24 / interval_hours:.0f}")
    print(f"  Press Ctrl+C to stop")
    print("="*60)
    
    while True:
        try:
            await run_vibe_cycle(max_iterations=5)
            
            next_run = datetime.utcnow().timestamp() + (interval_hours * 3600)
            print(f"\n💤 Sleeping until {datetime.fromtimestamp(next_run).isoformat()}")
            print(f"   (Next app in {interval_hours} hours)")
            
            await asyncio.sleep(interval_hours * 3600)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping daemon...")
            break
        except Exception as e:
            print(f"\n❌ Error in cycle: {e}")
            print("   Retrying in 1 hour...")
            await asyncio.sleep(3600)


def show_status():
    """Show vibe coder status."""
    print("\n" + "="*60)
    print("  🎨 VIBE CODER - Status")
    print("="*60)
    
    history_file = os.path.join(os.path.dirname(__file__), 'state', 'history.json')
    
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
        
        total_cycles = len(history)
        total_apps = sum(h.get('apps_generated', 0) for h in history)
        total_duplicates = sum(h.get('duplicates_skipped', 0) for h in history)
        
        print(f"  Total cycles: {total_cycles}")
        print(f"  Total apps generated: {total_apps}")
        print(f"  Total duplicates skipped: {total_duplicates}")
        
        if history:
            last_cycle = history[-1]
            print(f"\n  Last cycle:")
            print(f"    Time: {last_cycle.get('cycle_end', 'N/A')}")
            print(f"    Apps: {last_cycle.get('apps_generated', 0)}")
    else:
        print("  No cycles run yet")
    
    # Show recent apps
    projects_dir = os.path.join(os.path.dirname(__file__), 'projects')
    if os.path.exists(projects_dir):
        projects = os.listdir(projects_dir)
        if projects:
            print(f"\n  Recent apps ({len(projects)} total):")
            for proj in projects[-5:]:
                print(f"    - {proj}")
    
    print("="*60)


def list_apps():
    """List all generated apps."""
    print("\n" + "="*60)
    print("  🎨 Generated Apps")
    print("="*60)
    
    projects_dir = os.path.join(os.path.dirname(__file__), 'projects')
    
    if not os.path.exists(projects_dir):
        print("  No apps generated yet")
        return
    
    for project in sorted(os.listdir(projects_dir)):
        project_path = os.path.join(projects_dir, project)
        if os.path.isdir(project_path):
            readme_path = os.path.join(project_path, 'README.md')
            
            print(f"\n📦 {project}")
            
            if os.path.exists(readme_path):
                with open(readme_path, 'r') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('#'):
                        print(f"   {first_line[1:].strip()}")
            
            print(f"   Path: {project_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Vibe Coder - Autonomous App Factory"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run single cycle')
    run_parser.add_argument(
        '--max-ideas', '-n',
        type=int,
        default=5,
        help='Maximum ideas to process'
    )
    
    # Daemon command
    daemon_parser = subparsers.add_parser('daemon', help='Run continuously')
    daemon_parser.add_argument(
        '--interval', '-i',
        type=float,
        default=4.0,
        help='Hours between cycles'
    )
    
    # Status command
    subparsers.add_parser('status', help='Show status')
    
    # List command
    subparsers.add_parser('list', help='List generated apps')
    
    args = parser.parse_args()
    
    if args.command == 'run' or args.command is None:
        asyncio.run(run_vibe_cycle(getattr(args, 'max_ideas', 5)))
    
    elif args.command == 'daemon':
        asyncio.run(run_daemon(args.interval))
    
    elif args.command == 'status':
        show_status()
    
    elif args.command == 'list':
        list_apps()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
