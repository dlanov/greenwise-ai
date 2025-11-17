from typing import Any, Dict

from config import GreenWiseConfig
from tools.base_tool import BaseTool

class EmissionsCalculator(BaseTool):
    """Tool for calculating CO2 emissions"""
    
    def __init__(self):
        super().__init__(
            name="emissions_calculator",
            description="Calculate CO2 emissions from energy consumption or fuel usage"
        )
        self.config = GreenWiseConfig()
    
    async def execute(self, energy_kwh: float = 0, fuel_type: str = None,
                     fuel_liters: float = 0) -> Dict[str, Any]:
        """
        Calculate emissions
        
        Args:
            energy_kwh: Electricity consumption in kWh
            fuel_type: Type of fuel (diesel, gasoline)
            fuel_liters: Fuel consumption in liters
        
        Returns:
            Dict with co2_kg and breakdown
        """
        total_co2 = 0
        breakdown = {}
        
        # Electricity emissions
        if energy_kwh > 0:
            co2_from_electricity = energy_kwh * self.config.EMISSION_FACTOR_ELECTRICITY
            total_co2 += co2_from_electricity
            breakdown["electricity"] = {
                "kwh": energy_kwh,
                "co2_kg": co2_from_electricity,
                "factor": self.config.EMISSION_FACTOR_ELECTRICITY
            }
        
        # Fuel emissions
        if fuel_type and fuel_liters > 0:
            if fuel_type.lower() == "diesel":
                factor = self.config.EMISSION_FACTOR_DIESEL
            elif fuel_type.lower() == "gasoline":
                factor = self.config.EMISSION_FACTOR_GASOLINE
            else:
                factor = 2.5  # default
            
            co2_from_fuel = fuel_liters * factor
            total_co2 += co2_from_fuel
            breakdown[fuel_type] = {
                "liters": fuel_liters,
                "co2_kg": co2_from_fuel,
                "factor": factor
            }
        
        return {
            "co2_kg": total_co2,
            "breakdown": breakdown
        }
    
    def get_parameters_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "energy_kwh": {
                    "type": "number",
                    "description": "Electricity consumption in kWh"
                },
                "fuel_type": {
                    "type": "string",
                    "enum": ["diesel", "gasoline"],
                    "description": "Type of fuel"
                },
                "fuel_liters": {
                    "type": "number",
                    "description": "Fuel consumption in liters"
                }
            }
        }
