import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class GreenWiseConfig:
    """Central configuration for GreenWise AI"""
    
    # API Keys (from environment or Hugging Face Secrets)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    
    # LLM Configuration
    MODEL_NAME: str = "gemini-2.0-flash-exp"  # or gemini-pro
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2048
    
    # Memory Configuration
    MEMORY_BACKEND: str = "sqlite"  # For HF Spaces: sqlite or json
    MEMORY_PATH: str = "./data/memory.db"
    
    # Operational Parameters
    EMISSION_FACTOR_ELECTRICITY: float = 0.475  # kg CO2/kWh (avg grid)
    EMISSION_FACTOR_DIESEL: float = 2.68  # kg CO2/L
    EMISSION_FACTOR_GASOLINE: float = 2.31  # kg CO2/L
    
    # Dashboard Settings
    REFRESH_INTERVAL: int = 300  # seconds
    MAX_RECOMMENDATIONS: int = 10
    
    # Feature Flags
    ENABLE_WEATHER_API: bool = False  # Set to True when API key available
    ENABLE_ROUTE_OPTIMIZATION: bool = True
    ENABLE_AUTO_ACTIONS: bool = False  # Require user approval
