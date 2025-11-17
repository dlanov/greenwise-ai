"""
memory/session_manager.py

Manages user sessions and temporary state.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

@dataclass
class Session:
    """Represents a user session."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)
    
    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.now()
    
    def get(self, key: str, default=None):
        """Get session data."""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set session data."""
        self.data[key] = value
        self.update_activity()

class SessionManager:
    """Manages multiple user sessions."""
    
    def __init__(self):
        self._sessions: Dict[str, Session] = {}
    
    def create_session(self, user_id: Optional[str] = None) -> Session:
        """Create a new session."""
        session = Session(user_id=user_id)
        self._sessions[session.session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieve a session by ID."""
        return self._sessions.get(session_id)
    
    def delete_session(self, session_id: str):
        """Delete a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
    
    def cleanup_stale_sessions(self, max_age_hours: int = 24):
        """Remove sessions older than max_age_hours."""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        
        stale_ids = [
            sid for sid, session in self._sessions.items()
            if session.last_activity < cutoff
        ]
        
        for sid in stale_ids:
            del self._sessions[sid]
        
        return len(stale_ids)


# Export note for reference
INIT_FILES_SUMMARY = """
Summary of __init__.py files:

1. agents/__init__.py - Exports all agent classes
2. llm/__init__.py - Exports LLM client and prompts
3. tools/__init__.py - Tool registry with factory functions
4. memory/__init__.py - Memory components with singleton pattern
5. data/__init__.py - Data processing pipeline
6. ui/__init__.py - UI components
7. utils/__init__.py - Utility functions
8. Root __init__.py - Main package exports

Each __init__.py provides:
- Clean public API through __all__
- Version information
- Convenient imports
- Factory functions where appropriate
- Package documentation
"""
