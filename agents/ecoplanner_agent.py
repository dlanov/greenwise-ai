from datetime import datetime
from typing import Any, Dict, List

from agents.base_agent import BaseAgent
from config import GreenWiseConfig

class EcoPlannerAgent(BaseAgent):
    """Agent responsible for generating sustainability action plans"""
    
    async def execute(self, context_package: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main planning workflow:
        1. Analyze current situation
        2. Generate action candidates
        3. Evaluate with tools
        4. Prioritize recommendations
        5. Return actionable plan
        """
        self.logger.info("EcoPlanner: Starting planning cycle")
        
        # 1. Build LLM prompt with context
        prompt = self._build_planning_prompt(context_package)
        
        # 2. Generate initial recommendations using LLM
        llm_response = await self.llm_client.generate_with_tools(
            prompt=prompt,
            tools=list(self.tools.values()),
            context=context_package
        )
        
        # 3. Parse and structure recommendations
        recommendations = self._parse_recommendations(llm_response)
        
        # 4. Validate and enrich with tool calls
        enriched_recommendations = await self._enrich_recommendations(
            recommendations, 
            context_package
        )
        
        # 5. Prioritize and format output
        final_plan = self._prioritize_and_format(enriched_recommendations)
        
        # 6. Store in memory
        self.memory_bank.store_plan(final_plan)
        
        self.log_action("plan_generated", {
            "recommendation_count": len(final_plan["recommendations"]),
            "estimated_co2_savings": final_plan.get("total_co2_savings_kg", 0)
        })
        
        return final_plan
    
    def _build_planning_prompt(self, context: Dict[str, Any]) -> str:
        """Construct detailed prompt for Gemini"""
        from llm.prompt_templates import ECOPLANNER_SYSTEM_PROMPT
        
        summary = context.get("operational_summary", {})
        anomalies = context.get("anomalies", [])
        external = context.get("external_context", {})
        
        prompt = f"""{ECOPLANNER_SYSTEM_PROMPT}

## Current Operational State

**Total Energy Consumption:** {summary.get('total_energy_kwh', 0):.1f} kWh
**Total CO2 Emissions:** {summary.get('total_emissions_kg_co2', 0):.1f} kg CO2
**Detected Anomalies:** {len(anomalies)}

### Anomalies Requiring Attention:
"""
        for anomaly in anomalies[:5]:  # Top 5
            prompt += f"\n- {anomaly['type']} at {anomaly['facility']}: "
            prompt += f"{anomaly['deviation_pct']:.1f}% above baseline (severity: {anomaly['severity']})"
        
        prompt += f"""

### External Context:
- Grid Carbon Intensity: {external.get('grid_carbon_intensity', 0.5):.2f} kg CO2/kWh
"""
        
        if "weather" in external:
            weather = external["weather"]
            prompt += f"- Weather Forecast: {weather.get('condition', 'N/A')}, "
            prompt += f"Temp: {weather.get('temperature', 'N/A')}°C\n"
        
        prompt += """

## Task:
Generate 3-5 specific, actionable recommendations to:
1. Reduce energy consumption
2. Lower carbon emissions
3. Improve operational efficiency
4. Address detected anomalies

For each recommendation, provide:
- Clear action description
- Estimated impact (kWh saved, CO2 reduced)
- Implementation complexity (low/medium/high)
- Time horizon (immediate/short-term/long-term)

Use available tools to calculate precise impacts when needed.
"""
        return prompt
    
    def _parse_recommendations(self, llm_response: Dict) -> List[Dict[str, Any]]:
        """Parse LLM output into structured recommendations"""
        # Extract recommendations from LLM response
        # Handle both text and structured outputs
        text = llm_response.get("text", "")
        tool_calls = llm_response.get("tool_calls", [])
        
        # Simple parsing (in production, use more robust parsing)
        recommendations = []
        
        # Example structured output
        if "recommendations" in llm_response:
            return llm_response["recommendations"]
        
        # Parse from text (fallback)
        lines = text.split("\n")
        current_rec = {}
        
        for line in lines:
            if line.startswith("##") or line.startswith("**Recommendation"):
                if current_rec:
                    recommendations.append(current_rec)
                current_rec = {"description": "", "impact": {}}
            elif current_rec:
                current_rec["description"] += line + " "
        
        if current_rec:
            recommendations.append(current_rec)
        
        return recommendations
    
    async def _enrich_recommendations(
        self, 
        recommendations: List[Dict], 
        context: Dict
    ) -> List[Dict[str, Any]]:
        """Enrich recommendations with tool-calculated impacts"""
        enriched = []
        
        for rec in recommendations:
            # Calculate emissions impact
            if "emissions_calculator" in self.tools:
                impact = await self.tools["emissions_calculator"].execute(
                    energy_kwh=rec.get("energy_savings_kwh", 0)
                )
                rec["co2_savings_kg"] = impact.get("co2_kg", 0)
            
            # Optimize routes if applicable
            if "route" in rec.get("description", "").lower():
                if "route_optimizer" in self.tools:
                    route_result = await self.tools["route_optimizer"].optimize(
                        rec.get("route_params", {})
                    )
                    rec["route_optimization"] = route_result
            
            enriched.append(rec)
        
        return enriched
    
    def _prioritize_and_format(self, recommendations: List[Dict]) -> Dict[str, Any]:
        """Prioritize by impact and format final output"""
        # Sort by CO2 savings (descending)
        sorted_recs = sorted(
            recommendations,
            key=lambda x: x.get("co2_savings_kg", 0),
            reverse=True
        )
        
        total_co2_savings = sum(r.get("co2_savings_kg", 0) for r in sorted_recs)
        total_energy_savings = sum(r.get("energy_savings_kwh", 0) for r in sorted_recs)

        config = GreenWiseConfig()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "recommendations": sorted_recs[:config.MAX_RECOMMENDATIONS],
            "total_co2_savings_kg": total_co2_savings,
            "total_energy_savings_kwh": total_energy_savings,
            "implementation_priority": "high" if total_co2_savings > 100 else "medium"
        }
