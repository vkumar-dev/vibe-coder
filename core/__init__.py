"""
Vibe Coder Core Modules
"""

from core.research import ResearchAgent, Trend, AppIdea
from core.duplicate_checker import DuplicateChecker, DuplicateCheck
from core.generator import AppGenerator, AppGenerationResult

__all__ = [
    'ResearchAgent',
    'Trend',
    'AppIdea',
    'DuplicateChecker',
    'DuplicateCheck',
    'AppGenerator',
    'AppGenerationResult',
]
