#!/usr/bin/env python3
"""
Vibe Coder - Duplicate Checker

Checks if a similar project already exists in GitHub repos or local projects.
"""

import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from typing import List, Optional, Tuple


@dataclass
class DuplicateCheck:
    """Result of a duplicate check."""
    idea_id: str
    is_duplicate: bool
    similarity_score: float
    matching_projects: List[dict]
    checked_at: str


class DuplicateChecker:
    """Checks for duplicate projects."""
    
    def __init__(self, github_user: str = "vkumar-dev", config_path: str = "config.yaml"):
        self.github_user = github_user
        self.config_path = config_path
        self.local_projects_dir = os.path.join(os.path.dirname(__file__), '..', 'projects')
        self.state_file = os.path.join(os.path.dirname(__file__), '..', 'state', 'duplicates.json')
        
    def check_github_repos(self, idea_title: str, idea_description: str) -> Tuple[bool, List[dict], float]:
        """Check GitHub repos for similar projects."""
        print(f"🔍 Checking GitHub repos for duplicates...")
        
        matching_repos = []
        max_similarity = 0.0
        
        try:
            # Get all user repos
            result = subprocess.run(
                ["gh", "repo", "list", self.github_user, "--limit", "100", "--json", "name,description"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                repos = json.loads(result.stdout)
                
                for repo in repos:
                    # Check name similarity
                    name_similarity = self._calculate_similarity(idea_title, repo['name'])
                    
                    # Check description similarity
                    desc_similarity = 0.0
                    if repo.get('description'):
                        desc_similarity = self._calculate_similarity(idea_description, repo['description'])
                    
                    # Take max of name and description similarity
                    similarity = max(name_similarity, desc_similarity)
                    
                    if similarity > 0.5:  # Threshold for potential duplicate
                        matching_repos.append({
                            'source': 'github',
                            'name': repo['name'],
                            'description': repo.get('description', ''),
                            'similarity': similarity
                        })
                        max_similarity = max(max_similarity, similarity)
        except Exception as e:
            print(f"⚠️  GitHub check error: {e}")
        
        is_duplicate = max_similarity > 0.7
        return is_duplicate, matching_repos, max_similarity
    
    def check_local_projects(self, idea_title: str, idea_description: str) -> Tuple[bool, List[dict], float]:
        """Check local projects directory for similar projects."""
        print(f"🔍 Checking local projects for duplicates...")
        
        matching_projects = []
        max_similarity = 0.0
        
        if not os.path.exists(self.local_projects_dir):
            return False, [], 0.0
        
        # Scan project directories
        for project_name in os.listdir(self.local_projects_dir):
            project_path = os.path.join(self.local_projects_dir, project_name)
            
            if os.path.isdir(project_path):
                # Check project name similarity
                name_similarity = self._calculate_similarity(idea_title, project_name)
                
                # Try to read README for description match
                desc_similarity = 0.0
                readme_path = os.path.join(project_path, 'README.md')
                if os.path.exists(readme_path):
                    try:
                        with open(readme_path, 'r') as f:
                            readme_content = f.read(500)  # First 500 chars
                            desc_similarity = self._calculate_similarity(idea_description, readme_content)
                    except Exception:
                        pass
                
                similarity = max(name_similarity, desc_similarity)
                
                if similarity > 0.5:
                    matching_projects.append({
                        'source': 'local',
                        'name': project_name,
                        'path': project_path,
                        'similarity': similarity
                    })
                    max_similarity = max(max_similarity, similarity)
        
        is_duplicate = max_similarity > 0.7
        return is_duplicate, matching_projects, max_similarity
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two strings."""
        if not text1 or not text2:
            return 0.0
        
        # Normalize texts
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        # Use SequenceMatcher for similarity
        return SequenceMatcher(None, text1_lower, text2_lower).ratio()
    
    def check_duplicate(self, idea_id: str, idea_title: str, idea_description: str) -> DuplicateCheck:
        """Run full duplicate check."""
        print(f"\n🔍 Checking duplicates for: {idea_title[:50]}...")
        
        # Check GitHub
        gh_duplicate, gh_matches, gh_score = self.check_github_repos(idea_title, idea_description)
        
        # Check local
        local_duplicate, local_matches, local_score = self.check_local_projects(idea_title, idea_description)
        
        # Combine results
        is_duplicate = gh_duplicate or local_duplicate
        max_score = max(gh_score, local_score)
        all_matches = gh_matches + local_matches
        
        check = DuplicateCheck(
            idea_id=idea_id,
            is_duplicate=is_duplicate,
            similarity_score=max_score,
            matching_projects=all_matches,
            checked_at=datetime.utcnow().isoformat()
        )
        
        # Save to state
        self._save_check(check)
        
        if is_duplicate:
            print(f"⚠️  DUPLICATE DETECTED (similarity: {max_score:.2f})")
            for match in all_matches:
                print(f"   - {match['source']}: {match['name']} ({match['similarity']:.2f})")
        else:
            print(f"✅ No duplicates found (max similarity: {max_score:.2f})")
        
        return check
    
    def _save_check(self, check: DuplicateCheck):
        """Save check result to state file."""
        state_dir = os.path.join(os.path.dirname(__file__), '..', 'state')
        os.makedirs(state_dir, exist_ok=True)
        
        # Load existing checks
        checks = []
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    checks = json.load(f)
            except Exception:
                checks = []
        
        # Add new check
        checks.append({
            'idea_id': check.idea_id,
            'is_duplicate': check.is_duplicate,
            'similarity_score': check.similarity_score,
            'matching_projects': check.matching_projects,
            'checked_at': check.checked_at
        })
        
        # Save (keep last 1000 checks)
        with open(self.state_file, 'w') as f:
            json.dump(checks[-1000:], f, indent=2)
    
    def get_previous_checks(self) -> List[dict]:
        """Get all previous duplicate checks."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return []


if __name__ == "__main__":
    checker = DuplicateChecker()
    
    # Test with a sample idea
    check = checker.check_duplicate(
        idea_id="test-001",
        idea_title="AI-powered code review tool",
        idea_description="Automated code review using AI to find bugs and suggest improvements"
    )
    
    print(f"\nResult: Duplicate={check.is_duplicate}, Score={check.similarity_score}")
