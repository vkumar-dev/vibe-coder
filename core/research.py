#!/usr/bin/env python3
"""
Vibe Coder - Research Agent

Researches trending topics and generates app ideas.
"""

import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import yaml


@dataclass
class Trend:
    """Represents a trending topic or opportunity."""
    id: str
    source: str
    title: str
    description: str
    url: str
    score: float
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class AppIdea:
    """Represents a generated app idea."""
    id: str
    title: str
    description: str
    trend_source: str
    features: List[str] = field(default_factory=list)
    tech_stack: dict = field(default_factory=dict)
    priority: float = 0.0
    is_ai_infused: bool = True
    ai_capabilities: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class ResearchAgent:
    """Researches trends and generates app ideas."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.trends: List[Trend] = []
        self.ideas: List[AppIdea] = []
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        config_file = os.path.join(os.path.dirname(__file__), config_path)
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def research_github_trending(self) -> List[Trend]:
        """Fetch trending repositories from GitHub."""
        print("🔍 Researching GitHub trending...")
        trends = []
        
        try:
            # Use gh CLI to get trending repos
            result = subprocess.run(
                ["gh", "search", "repos", 
                 "--sort", "stars", 
                 "--order", "desc",
                 "--limit", "20",
                 "--json", "name,description,url,createdAt,primaryLanguage,nameWithOwner"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                repos = json.loads(result.stdout)
                for repo in repos[:10]:
                    trend = Trend(
                        id=f"gh-{repo['nameWithOwner'].replace('/', '-')}",
                        source="github_trending",
                        title=repo['name'],
                        description=repo.get('description', '') or 'No description',
                        url=repo['url'],
                        score=8.0,  # Base score for trending repos
                        tags=[repo.get('primaryLanguage', {}).get('name', 'unknown')] if repo.get('primaryLanguage') else []
                    )
                    trends.append(trend)
        except Exception as e:
            print(f"⚠️  GitHub trending error: {e}")
        
        self.trends.extend(trends)
        return trends
    
    def research_product_hunt(self) -> List[Trend]:
        """Research Product Hunt for trending products."""
        print("🔍 Researching Product Hunt...")
        trends = []
        
        try:
            # Use web search via gh or direct API if available
            # For now, use a placeholder pattern
            result = subprocess.run(
                ["gh", "api", "/search/issues",
                 "-q", "product hunt launch",
                 "--limit", "10"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Parse results
                pass
        except Exception as e:
            print(f"⚠️  Product Hunt research error: {e}")
        
        return trends
    
    def research_hacker_news(self) -> List[Trend]:
        """Research Hacker News for trending topics."""
        print("🔍 Researching Hacker News...")
        trends = []
        
        try:
            # Fetch HN stories via API
            import urllib.request
            import json as json_lib
            
            # Get top stories
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            with urllib.request.urlopen(url, timeout=10) as response:
                top_ids = json_lib.loads(response.read())[:20]
            
            # Fetch story details
            for story_id in top_ids[:10]:
                try:
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    with urllib.request.urlopen(story_url, timeout=10) as response:
                        story = json_lib.loads(response.read())
                    
                    if story and story.get('title'):
                        trend = Trend(
                            id=f"hn-{story_id}",
                            source="hacker_news",
                            title=story['title'],
                            description=story.get('text', '')[:200] if story.get('text') else '',
                            url=story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            score=min(10.0, story.get('score', 0) / 100),
                            tags=["hacker_news"]
                        )
                        trends.append(trend)
                except Exception:
                    continue
        except Exception as e:
            print(f"⚠️  Hacker News research error: {e}")
        
        self.trends.extend(trends)
        return trends
    
    def generate_app_ideas(self, max_ideas: int = 5) -> List[AppIdea]:
        """Generate app ideas from researched trends."""
        print(f"💡 Generating app ideas from {len(self.trends)} trends...")
        
        # Sort trends by score
        sorted_trends = sorted(self.trends, key=lambda t: t.score, reverse=True)
        
        ideas = []
        for i, trend in enumerate(sorted_trends[:max_ideas]):
            # Prioritize AI-infused apps (70% AI, 30% any viral app)
            should_be_ai = (i % 3 != 0)  # Every 3rd app can be non-AI
            
            if should_be_ai:
                idea = self._generate_ai_app_idea(trend, i)
            else:
                idea = self._generate_viral_app_idea(trend, i)
            
            ideas.append(idea)
        
        self.ideas = ideas
        return self.ideas
    
    def _generate_ai_app_idea(self, trend: Trend, index: int) -> AppIdea:
        """Generate an AI-infused app idea."""
        ai_features = [
            ("Natural language processing", "NLP"),
            ("Computer vision", "CV"),
            ("Predictive analytics", "ML"),
            ("Generative AI content", "GenAI"),
            ("Voice/speech recognition", "ASR"),
            ("Recommendation engine", "RecSys"),
            ("Automated decision making", "Agent"),
            ("Smart automation", "Agent"),
            ("Personalization engine", "ML"),
            ("Sentiment analysis", "NLP"),
        ]
        
        # Pick AI capability based on trend
        ai_cap = ai_features[index % len(ai_features)]
        
        return AppIdea(
            id=f"ai-idea-{trend.id}",
            title=f"AI-Powered: {trend.title[:40]}",
            description=f"AI-infused app with {ai_cap[0]} inspired by: {trend.description[:80]}",
            trend_source=trend.source,
            features=[
                f"{ai_cap[0]} integration",
                "Smart automation with AI agents",
                "Real-time AI inference",
                "Personalized user experience",
                "Continuous learning from user behavior"
            ],
            tech_stack={
                "frontend": "react",
                "backend": "node",
                "database": "sqlite",
                "ai": ["langchain", "transformers", "openai-api"]
            },
            priority=trend.score + 1.0,  # Boost AI apps
            is_ai_infused=True,
            ai_capabilities=[ai_cap[0], ai_cap[1]]
        )
    
    def _generate_viral_app_idea(self, trend: Trend, index: int) -> AppIdea:
        """Generate a viral-potential app idea (non-AI or minimal AI)."""
        return AppIdea(
            id=f"viral-idea-{trend.id}",
            title=f"Viral App: {trend.title[:40]}",
            description=f"Simple, addictive app inspired by: {trend.description[:80]}",
            trend_source=trend.source,
            features=[
                "Clean, intuitive UI",
                "Gamification elements",
                "Social sharing built-in",
                "Instant gratification",
                "Mobile-first design"
            ],
            tech_stack={
                "frontend": "react",
                "backend": "node",
                "database": "sqlite"
            },
            priority=trend.score,
            is_ai_infused=False,
            ai_capabilities=[]
        )
    
    def run_full_research(self) -> dict:
        """Run complete research cycle."""
        print("\n" + "="*60)
        print("  🔬 VIBE CODER - Research Phase")
        print("="*60)
        
        # Run all research sources
        self.research_github_trending()
        self.research_hacker_news()
        
        # Generate ideas
        ideas = self.generate_app_ideas()
        
        # Save trends to file
        self._save_trends()
        
        print(f"\n✅ Research complete:")
        print(f"   Trends found: {len(self.trends)}")
        print(f"   Ideas generated: {len(ideas)}")
        
        return {
            'trends': len(self.trends),
            'ideas': len(ideas),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _save_trends(self):
        """Save trends to state file."""
        state_dir = os.path.join(os.path.dirname(__file__), 'state')
        os.makedirs(state_dir, exist_ok=True)
        
        trends_file = os.path.join(state_dir, 'trends.json')
        data = {
            'updated_at': datetime.utcnow().isoformat(),
            'trends': [
                {
                    'id': t.id,
                    'source': t.source,
                    'title': t.title,
                    'score': t.score
                }
                for t in self.trends
            ]
        }
        
        with open(trends_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_trends(self) -> List[Trend]:
        """Load trends from state file."""
        state_dir = os.path.join(os.path.dirname(__file__), 'state')
        trends_file = os.path.join(state_dir, 'trends.json')
        
        if os.path.exists(trends_file):
            with open(trends_file, 'r') as f:
                data = json.load(f)
                return [Trend(**t) for t in data.get('trends', [])]
        
        return []


if __name__ == "__main__":
    agent = ResearchAgent()
    result = agent.run_full_research()
    print(f"\nResult: {result}")
