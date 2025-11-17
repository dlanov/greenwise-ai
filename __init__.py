"""
GreenWise AI - Sustainable Operations Orchestrator

An AI-powered multi-agent system for optimizing enterprise sustainability.
Uses Google Gemini LLM and specialized agents to:
- Monitor operational data
- Detect inefficiencies
- Generate actionable recommendations
- Track sustainability improvements

Main Components:
- Multi-agent orchestration (Data Scout + EcoPlanner)
- LLM-powered reasoning with tool integration
- Persistent memory and learning
- Interactive Gradio dashboard

Usage:
    from greenwise_ai import GreenWiseApp
    
    app = GreenWiseApp()
    app.launch()

Or run directly:
    python app.py
"""

from .config import GreenWiseConfig
from .app import GreenWiseApp

# Import key components for easy access
from .agents import (
    DataScoutAgent,
    EcoPlannerAgent,
    MultiAgentOrchestrator,
)
from .llm import GeminiClient
from .memory import MemoryBank
from .tools import get_all_tools

__version__ = '1.0.0'
__author__ = 'GreenWise AI Team'
__license__ = 'MIT'

__all__ = [
    # Main app
    'GreenWiseApp',
    'GreenWiseConfig',
    # Core components
    'DataScoutAgent',
    'EcoPlannerAgent',
    'MultiAgentOrchestrator',
    'GeminiClient',
    'MemoryBank',
    'get_all_tools',
]

# Package metadata
__package_name__ = 'greenwise-ai'
__description__ = 'AI-powered sustainable operations orchestrator'
__url__ = 'https://huggingface.co/spaces/YOUR_USERNAME/greenwise-ai'
