"""
LLM integration layer for GreenWise AI.

Handles interaction with Google Gemini and other language models,
including prompt management, context handling, and tool integration.
"""

from .gemini_client import GeminiClient
from .prompt_templates import (
    ECOPLANNER_SYSTEM_PROMPT,
    DATA_SCOUT_SYSTEM_PROMPT,
    RECOMMENDATION_FORMAT_TEMPLATE,
    ANALYSIS_PROMPT_TEMPLATE,
)
from .context_manager import ContextManager, ContextWindow

__all__ = [
    'GeminiClient',
    'ContextManager',
    'ContextWindow',
    'ECOPLANNER_SYSTEM_PROMPT',
    'DATA_SCOUT_SYSTEM_PROMPT',
    'RECOMMENDATION_FORMAT_TEMPLATE',
    'ANALYSIS_PROMPT_TEMPLATE',
]

__version__ = '1.0.0'
