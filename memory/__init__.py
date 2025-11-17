"""
Memory and persistence layer for GreenWise AI.

Manages:
- Operational context storage
- Historical data and trends
- User feedback and learning
- Session state management
"""

from .memory_bank import MemoryBank, MemoryEntry
from .session_manager import SessionManager, Session
from .vector_store import VectorStore  # Optional, for semantic search

__all__ = [
    'MemoryBank',
    'MemoryEntry',
    'SessionManager',
    'Session',
    'VectorStore',
]

__version__ = '1.0.0'

# Singleton instance for easy access
_memory_instance = None

def get_memory_bank(db_path: str = "./data/memory.db"):
    """Get or create singleton MemoryBank instance."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = MemoryBank(db_path)
    return _memory_instance
