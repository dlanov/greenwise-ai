from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Dict, Any

class BaseTool(ABC):
    """Base class for all tools (MCP-style interface)"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool's function"""
        pass
    
    def to_gemini_function(self) -> Dict:
        """Convert tool to Gemini function declaration format"""
        schema = self.get_parameters_schema() or {}
        normalized_schema = self._normalize_schema_for_gemini(deepcopy(schema))
        return {
            "name": self.name,
            "description": self.description,
            "parameters": normalized_schema
        }
    
    @abstractmethod
    def get_parameters_schema(self) -> Dict:
        """Return JSON schema for tool parameters"""
        pass

    def _normalize_schema_for_gemini(self, schema: Any) -> Any:
        """Recursively normalize JSON schema "type" values for Gemini."""
        if isinstance(schema, dict):
            normalized = {}
            for key, value in schema.items():
                if key == "type" and isinstance(value, str):
                    normalized[key] = value.upper()
                elif isinstance(value, dict):
                    normalized[key] = self._normalize_schema_for_gemini(value)
                elif isinstance(value, list):
                    normalized[key] = [
                        self._normalize_schema_for_gemini(item) for item in value
                    ]
                else:
                    normalized[key] = value
            return normalized

        if isinstance(schema, list):
            return [self._normalize_schema_for_gemini(item) for item in schema]

        return schema
