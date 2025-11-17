"""
agents/orchestrator.py

Multi-agent coordination and workflow orchestration.
"""

from typing import Dict, Any, List, Optional
import asyncio
import logging
from datetime import datetime

class MultiAgentOrchestrator:
    """
    Coordinates multiple agents to execute complex workflows.
    
    Manages agent lifecycle, communication, and task delegation.
    """
    
    def __init__(self, agents: List, memory_bank, config):
        self.agents = {agent.name: agent for agent in agents}
        self.memory_bank = memory_bank
        self.config = config
        self.logger = logging.getLogger("orchestrator")
        self._task_queue = asyncio.Queue()
    
    async def run_cycle(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute one complete orchestration cycle.
        
        1. Data Scout gathers context
        2. EcoPlanner generates recommendations
        3. Results stored and returned
        """
        self.logger.info("Starting orchestration cycle")
        
        try:
            # Phase 1: Data gathering
            if "DataScout" in self.agents:
                self.logger.info("Phase 1: Data Scout gathering context")
                context_package = await self.agents["DataScout"].execute(context or {})
            else:
                context_package = context or {}
            
            # Phase 2: Planning
            if "EcoPlanner" in self.agents:
                self.logger.info("Phase 2: EcoPlanner generating recommendations")
                plan = await self.agents["EcoPlanner"].execute(context_package)
            else:
                plan = {"error": "EcoPlanner not available"}
            
            # Phase 3: Store results
            self.memory_bank.store_orchestration_result({
                "timestamp": datetime.now().isoformat(),
                "context": context_package,
                "plan": plan,
                "status": "completed"
            })
            
            self.logger.info("Orchestration cycle completed successfully")
            return plan
            
        except Exception as e:
            self.logger.error(f"Orchestration cycle failed: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "status": "failed",
                "timestamp": datetime.now().isoformat()
            }
    
    async def parallel_execution(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute multiple agent tasks in parallel."""
        async_tasks = []
        
        for task in tasks:
            agent_name = task.get("agent")
            if agent_name in self.agents:
                async_tasks.append(
                    self.agents[agent_name].execute(task.get("context", {}))
                )
        
        results = await asyncio.gather(*async_tasks, return_exceptions=True)
        return results
    
    def add_agent(self, agent):
        """Dynamically add an agent to the orchestrator."""
        self.agents[agent.name] = agent
        self.logger.info(f"Added agent: {agent.name}")
    
    def remove_agent(self, agent_name: str):
        """Remove an agent from the orchestrator."""
        if agent_name in self.agents:
            del self.agents[agent_name]
            self.logger.info(f"Removed agent: {agent_name}")
