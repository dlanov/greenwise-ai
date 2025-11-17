"""
llm/context_manager.py

Manages LLM context window, token counting, and context optimization.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import tiktoken

@dataclass
class ContextWindow:
    """Represents a context window with token limits."""
    max_tokens: int = 8000
    current_tokens: int = 0
    content: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.content is None:
            self.content = []

class ContextManager:
    """
    Manages context for LLM calls, ensuring token limits are respected.
    """
    
    def __init__(self, model_name: str = "gpt-4", max_tokens: int = 8000):
        self.model_name = model_name
        self.max_tokens = max_tokens
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except:
            # Fallback for Gemini or other models
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        try:
            return len(self.encoding.encode(text))
        except:
            # Rough estimate: 1 token ≈ 4 characters
            return len(text) // 4
    
    def build_context(self, 
                     system_prompt: str,
                     current_data: Dict[str, Any],
                     history: Optional[List[Dict]] = None,
                     max_history_items: int = 5) -> str:
        """
        Build optimized context that fits within token limits.
        
        Priority:
        1. System prompt (always included)
        2. Current data (critical)
        3. Recent history (as much as fits)
        """
        context_parts = []
        remaining_tokens = self.max_tokens
        
        # 1. System prompt
        system_tokens = self.count_tokens(system_prompt)
        if system_tokens > remaining_tokens * 0.3:
            raise ValueError("System prompt too long")
        
        context_parts.append(system_prompt)
        remaining_tokens -= system_tokens
        
        # 2. Current data
        current_data_str = self._format_data(current_data)
        current_tokens = self.count_tokens(current_data_str)
        
        if current_tokens > remaining_tokens * 0.5:
            # Truncate current data if too large
            current_data_str = self._truncate_data(current_data_str, int(remaining_tokens * 0.5))
            current_tokens = self.count_tokens(current_data_str)
        
        context_parts.append(current_data_str)
        remaining_tokens -= current_tokens
        
        # 3. History (most recent first)
        if history:
            history_str = self._format_history(history, max_history_items)
            history_tokens = self.count_tokens(history_str)
            
            if history_tokens <= remaining_tokens:
                context_parts.append(history_str)
            else:
                # Include as much history as fits
                truncated_history = self._truncate_history(history, remaining_tokens)
                context_parts.append(truncated_history)
        
        return "\n\n".join(context_parts)
    
    def _format_data(self, data: Dict[str, Any]) -> str:
        """Format data dictionary as readable text."""
        import json
        return json.dumps(data, indent=2)
    
    def _format_history(self, history: List[Dict], max_items: int) -> str:
        """Format history entries."""
        recent = history[-max_items:] if len(history) > max_items else history
        formatted = ["## Historical Context\n"]
        
        for i, entry in enumerate(recent, 1):
            formatted.append(f"### Entry {i}")
            formatted.append(f"Timestamp: {entry.get('timestamp', 'N/A')}")
            formatted.append(f"Summary: {entry.get('summary', 'N/A')}\n")
        
        return "\n".join(formatted)
    
    def _truncate_data(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit token limit."""
        tokens = self.encoding.encode(text)
        if len(tokens) <= max_tokens:
            return text
        
        truncated_tokens = tokens[:max_tokens]
        return self.encoding.decode(truncated_tokens) + "\n... (truncated)"
    
    def _truncate_history(self, history: List[Dict], max_tokens: int) -> str:
        """Include as many recent history items as fit."""
        items = []
        current_tokens = 0
        
        for entry in reversed(history):
            entry_str = f"- {entry.get('timestamp')}: {entry.get('summary', '')}"
            entry_tokens = self.count_tokens(entry_str)
            
            if current_tokens + entry_tokens > max_tokens:
                break
            
            items.insert(0, entry_str)
            current_tokens += entry_tokens
        
        return "## Recent History\n" + "\n".join(items)
