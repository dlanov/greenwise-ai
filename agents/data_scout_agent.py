import asyncio
from datetime import datetime, timedelta
import numpy as np

class DataScoutAgent(BaseAgent):
    """Agent responsible for data aggregation and context preparation"""
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution flow:
        1. Ingest latest data
        2. Detect anomalies
        3. Summarize metrics
        4. Fetch external context
        5. Update memory bank
        """
        self.logger.info("DataScout: Starting data scouting cycle")
        
        # 1. Get latest operational data
        operational_data = await self._ingest_data(context.get("data_sources", {}))
        
        # 2. Detect anomalies
        anomalies = self._detect_anomalies(operational_data)
        
        # 3. Generate summary statistics
        summary = self._generate_summary(operational_data, anomalies)
        
        # 4. Fetch external context (weather, grid intensity, etc.)
        external_context = await self._fetch_external_context(context)
        
        # 5. Prepare context package for EcoPlanner
        context_package = {
            "timestamp": datetime.now().isoformat(),
            "operational_summary": summary,
            "anomalies": anomalies,
            "external_context": external_context,
            "historical_baseline": self._get_baseline_metrics()
        }
        
        # 6. Update memory bank
        self.memory_bank.store_context(context_package)
        
        self.log_action("context_prepared", {
            "anomaly_count": len(anomalies),
            "summary_metrics": list(summary.keys())
        })
        
        return context_package
    
    async def _ingest_data(self, data_sources: Dict) -> Dict[str, Any]:
        """Ingest data from various sources (IoT, databases, APIs)"""
        # In HF Spaces, use simulated data or uploaded files
        if "iot_tool" in self.tools:
            iot_data = await self.tools["iot_tool"].get_latest_readings()
        else:
            iot_data = self._generate_mock_data()
        
        return {
            "energy_consumption": iot_data.get("energy", {}),
            "emissions": iot_data.get("emissions", {}),
            "production_metrics": iot_data.get("production", {}),
            "facility_status": iot_data.get("facility", {})
        }
    
    def _detect_anomalies(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect operational anomalies using statistical methods"""
        anomalies = []
        
        # Example: Energy consumption anomaly detection
        energy_data = data.get("energy_consumption", {})
        for facility, readings in energy_data.items():
            current = readings.get("current_kwh", 0)
            baseline = readings.get("baseline_kwh", 0)
            
            if current > baseline * 1.15:  # 15% threshold
                anomalies.append({
                    "type": "energy_spike",
                    "facility": facility,
                    "current": current,
                    "baseline": baseline,
                    "deviation_pct": ((current - baseline) / baseline) * 100,
                    "severity": "high" if current > baseline * 1.3 else "medium"
                })
        
        return anomalies
    
    def _generate_summary(self, data: Dict, anomalies: List) -> Dict[str, Any]:
        """Generate natural language summary of current state"""
        return {
            "total_energy_kwh": self._sum_energy(data),
            "total_emissions_kg_co2": self._calculate_emissions(data),
            "anomaly_count": len(anomalies),
            "critical_facilities": self._identify_critical_facilities(data),
            "efficiency_metrics": self._calculate_efficiency(data)
        }
    
    async def _fetch_external_context(self, context: Dict) -> Dict[str, Any]:
        """Fetch weather, grid intensity, and other external data"""
        external = {}
        
        # Weather data
        if "weather_tool" in self.tools:
            external["weather"] = await self.tools["weather_tool"].get_forecast()
        
        # Grid carbon intensity (mock for demo)
        external["grid_carbon_intensity"] = self._get_grid_intensity()
        
        return external
    
    def _get_baseline_metrics(self) -> Dict[str, float]:
        """Retrieve historical baseline from memory"""
        return self.memory_bank.get_baseline_metrics()
    
    def _generate_mock_data(self) -> Dict[str, Any]:
        """Generate realistic mock IoT data for demo"""
        return {
            "energy": {
                "facility_a": {
                    "current_kwh": np.random.normal(500, 50),
                    "baseline_kwh": 450,
                    "hvac_kwh": np.random.normal(200, 20),
                    "lighting_kwh": np.random.normal(100, 10)
                },
                "facility_b": {
                    "current_kwh": np.random.normal(800, 80),
                    "baseline_kwh": 750,
                    "hvac_kwh": np.random.normal(350, 35),
                    "production_kwh": np.random.normal(400, 40)
                }
            },
            "emissions": {},
            "production": {},
            "facility": {}
        }
    
    def _sum_energy(self, data: Dict) -> float:
        """Calculate total energy consumption"""
        total = 0
        for facility_data in data.get("energy_consumption", {}).values():
            total += facility_data.get("current_kwh", 0)
        return total
    
    def _calculate_emissions(self, data: Dict) -> float:
        """Calculate total emissions"""
        config = GreenWiseConfig()
        total_kwh = self._sum_energy(data)
        return total_kwh * config.EMISSION_FACTOR_ELECTRICITY
    
    def _identify_critical_facilities(self, data: Dict) -> List[str]:
        """Identify facilities needing attention"""
        critical = []
        for facility, readings in data.get("energy_consumption", {}).items():
            if readings.get("current_kwh", 0) > readings.get("baseline_kwh", 0) * 1.2:
                critical.append(facility)
        return critical
    
    def _calculate_efficiency(self, data: Dict) -> Dict[str, float]:
        """Calculate operational efficiency metrics"""
        return {
            "energy_intensity": 1.2,  # kWh per unit output
            "capacity_utilization": 0.85
        }
    
    def _get_grid_intensity(self) -> float:
        """Get current grid carbon intensity (mock)"""
        # In production, call real API
        # Time-of-day variation simulation
        hour = datetime.now().hour
        if 10 <= hour <= 16:  # Solar peak
            return 0.35  # kg CO2/kWh
        else:
            return 0.55  # kg CO2/kWh
