from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, llm_client, memory_bank, tools: List):
        self.name = name
        self.llm_client = llm_client
        self.memory_bank = memory_bank
        self.tools = {tool.name: tool for tool in tools}
        self.logger = logging.getLogger(f"agent.{name}")
        
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent's main task"""
        pass
    
    def log_action(self, action: str, details: Dict[str, Any]):
        """Log agent actions for observability"""
        self.logger.info(f"{self.name}: {action}", extra=details)
        self.memory_bank.log_event(self.name, action, details)
