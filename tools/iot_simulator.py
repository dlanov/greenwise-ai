from typing import Any, Dict

import numpy as np

from tools.base_tool import BaseTool

class IoTSimulator(BaseTool):
    """Simulate IoT sensor data for demo purposes"""
    
    def __init__(self):
        super().__init__(
            name="iot_simulator",
            description="Get simulated IoT sensor readings from facilities"
        )
    
    async def get_latest_readings(self) -> Dict[str, Any]:
        """Generate realistic sensor data"""
        return {
            "energy": {
                "facility_a": {
                    "current_kwh": np.random.normal(500, 50),
                    "baseline_kwh": 450,
                    "hvac_kwh": np.random.normal(200, 20),
                    "lighting_kwh": np.random.normal(100, 10),
                    "equipment_kwh": np.random.normal(200, 30)
                },
                "facility_b": {
                    "current_kwh": np.random.normal(800, 80),
                    "baseline_kwh": 750,
                    "hvac_kwh": np.random.normal(350, 35),
                    "production_kwh": np.random.normal(400, 40),
                    "lighting_kwh": np.random.normal(50, 10)
                },
                "facility_c": {
                    "current_kwh": np.random.normal(300, 30),
                    "baseline_kwh": 320,
                    "hvac_kwh": np.random.normal(150, 15),
                    "lighting_kwh": np.random.normal(80, 10),
                    "equipment_kwh": np.random.normal(70, 10)
                }
            },
            "emissions": {},
            "production": {
                "facility_b": {
                    "units_produced": np.random.randint(800, 1200),
                    "efficiency": np.random.uniform(0.75, 0.95)
                }
            },
            "facility": {
                "facility_a": {
                    "temperature_c": np.random.uniform(20, 24),
                    "occupancy": np.random.randint(0, 150)
                },
                "facility_b": {
                    "temperature_c": np.random.uniform(18, 26),
                    "occupancy": np.random.randint(20, 100)
                },
                "facility_c": {
                    "temperature_c": np.random.uniform(21, 23),
                    "occupancy": np.random.randint(10, 80)
                }
            }
        }
    
    async def execute(self, facility_id: str = None) -> Dict[str, Any]:
        """Execute tool - get readings"""
        data = await self.get_latest_readings()
        
        if facility_id:
            return {
                "facility_id": facility_id,
                "energy": data["energy"].get(facility_id, {}),
                "facility_status": data["facility"].get(facility_id, {})
            }
        
        return data
    
    def get_parameters_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "facility_id": {
                    "type": "string",
                    "description": "Specific facility ID to query",
                    "enum": ["facility_a", "facility_b", "facility_c"]
                }
            }
        }
