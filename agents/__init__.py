"""
Multi-agent orchestration system for GreenWise AI.

This package contains specialized AI agents that work together to:
- Gather and analyze operational data (Data Scout)
- Generate sustainability recommendations (EcoPlanner)
- Orchestrate workflows between agents
"""

from .base_agent import BaseAgent
from .data_scout_agent import DataScoutAgent
from .ecoplanner_agent import EcoPlannerAgent
from .orchestrator import MultiAgentOrchestrator

__all__ = [
    'BaseAgent',
    'DataScoutAgent',
    'EcoPlannerAgent',
    'MultiAgentOrchestrator',
]

__version__ = '1.0.0'
