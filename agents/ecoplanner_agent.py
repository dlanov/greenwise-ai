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
        # 3b. If the LLM failed or returned an empty payload, fall back
        # to deterministic, rule-based recommendations. This ensures the
        # app still produces meaningful demo data even without a live LLM
        # connection or when the API response cannot be parsed.
        if not recommendations:
            recommendations = self._generate_rule_based_recommendations(context_package)
        # 4. Validate and enrich with tool calls
        enriched_recommendations = await self._enrich_recommendations(
            recommendations,
            context_package
        )
        if not enriched_recommendations:
            enriched_recommendations = self._generate_rule_based_recommendations(context_package)
        # 5. Prioritize and format output
        final_plan = self._prioritize_and_format(enriched_recommendations)
        
        # 6. Store in memory
        plan_id = self.memory_bank.store_plan(final_plan)
        final_plan["plan_id"] = plan_id
        
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
    def _generate_rule_based_recommendations(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate deterministic recommendations using heuristics.

        This is used whenever the LLM is unavailable so the UI still
        surfaces realistic demo data.
        """

        config = GreenWiseConfig()
        summary = context.get("operational_summary", {})
        anomalies = context.get("anomalies", [])
        baseline = context.get("historical_baseline", {})
        external_context = context.get("external_context", {})

        total_energy = summary.get("total_energy_kwh") or baseline.get("energy_kwh", 950)
        total_emissions = summary.get("total_emissions_kg_co2") or (
            total_energy * config.EMISSION_FACTOR_ELECTRICITY
        )
        grid_intensity = external_context.get(
            "grid_carbon_intensity",
            config.EMISSION_FACTOR_ELECTRICITY
        )

        recommendations: List[Dict[str, Any]] = []

        # HVAC scheduling / setback
        hvac_savings = round(max(total_energy * 0.08, 35), 1)
        recommendations.append({
            "id": "hvac_schedule_optimization",
            "description": (
                "Tighten HVAC scheduling with automatic after-hours setbacks "
                "and occupancy-based control. Target chillers and air handlers "
                "in administrative zones where loads stay high despite low night occupancy."
            ),
            "energy_savings_kwh": hvac_savings,
            "complexity": "medium",
            "timeline": "immediate",
            "category": "HVAC",
            "rationale": (
                "HVAC loads account for the majority of the current "
                f"{total_energy:.0f} kWh day. A 2-3°C setback outside occupied hours "
                "typically trims 6-10% without occupant impact."
            )
        })

        # Load shifting toward cleaner grid windows
        load_shift_savings = round(max(total_energy * 0.05, 25), 1)
        recommendations.append({
            "id": "load_shifting",
            "description": (
                "Reschedule non-critical production and charging tasks to the "
                "12:00-16:00 window when grid carbon intensity dips to "
                f"{grid_intensity:.2f} kg CO₂/kWh."
            ),
            "energy_savings_kwh": load_shift_savings,
            "complexity": "low",
            "timeline": "short-term",
            "category": "operations",
            "rationale": (
                "Flattening demand during peak-tariff hours avoids unnecessary "
                "compressor cycling and reduces marginal emissions by leveraging "
                "lower-carbon supply periods."
            )
        })

        # Anomaly-driven remediation
        for anomaly in anomalies[:3]:
            deviation = max(anomaly.get("current", 0) - anomaly.get("baseline", 0), 0)
            if deviation <= 0:
                continue

            rec_id = f"resolve_{anomaly.get('facility', 'facility')}_anomaly"
            energy_savings = round(max(deviation * 0.9, 20), 1)
            recommendations.append({
                "id": rec_id,
                "description": (
                    f"Investigate the {anomaly.get('type', 'energy')} pattern at "
                    f"{anomaly.get('facility', 'the facility')} and rebalance equipment loads."
                ),
                "energy_savings_kwh": energy_savings,
                "complexity": "medium" if anomaly.get("severity") == "high" else "low",
                "timeline": "immediate",
                "category": "anomaly_response",
                "rationale": (
                    f"Current draw is {anomaly.get('deviation_pct', 0):.1f}% above baseline. "
                    "Resetting setpoints and sequencing equipment typically recovers most of "
                    "the excess energy."
                )
            })

        # Lighting/controls tune-up as a default tertiary action
        lighting_savings = round(max(total_emissions * 0.04 / config.EMISSION_FACTOR_ELECTRICITY, 18), 1)
        recommendations.append({
            "id": "lighting_controls",
            "description": (
                "Calibrate occupancy sensors and daylight harvesting in common "
                "areas, and enforce automatic shutdown of decorative lighting."
            ),
            "energy_savings_kwh": lighting_savings,
            "complexity": "low",
            "timeline": "short-term",
            "category": "lighting",
            "rationale": (
                "Audit results show lighting persists near full output in multiple "
                "zones despite partial occupancy. Fine-tuning controls routinely "
                "captures 3-5% site-wide savings."
            )
        })

        return recommendations
