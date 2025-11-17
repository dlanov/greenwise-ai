"""
Tool integration system using MCP-style interface.

Provides standardized tools that agents can invoke for:
- Emissions calculations
- Route optimization
- Weather data
- IoT sensor access
- Benchmark data
"""

from .base_tool import BaseTool, ToolResult, ToolError
from .emissions_calculator import EmissionsCalculator
from .route_optimizer import RouteOptimizer
from .weather_api import WeatherAPI
from .iot_simulator import IoTSimulator
from .benchmark_data import BenchmarkDataTool

# Tool registry for easy access
AVAILABLE_TOOLS = {
    'emissions_calculator': EmissionsCalculator,
    'route_optimizer': RouteOptimizer,
    'weather_api': WeatherAPI,
    'iot_simulator': IoTSimulator,
    'benchmark_data': BenchmarkDataTool,
}

def get_tool(tool_name: str, **kwargs):
    """Factory function to instantiate tools by name."""
    if tool_name not in AVAILABLE_TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}. Available: {list(AVAILABLE_TOOLS.keys())}")
    return AVAILABLE_TOOLS[tool_name](**kwargs)

def get_all_tools(**config):
    """Get instances of all available tools."""
    return [tool_class(**config) for tool_class in AVAILABLE_TOOLS.values()]

__all__ = [
    'BaseTool',
    'ToolResult',
    'ToolError',
    'EmissionsCalculator',
    'RouteOptimizer',
    'WeatherAPI',
    'IoTSimulator',
    'BenchmarkDataTool',
    'AVAILABLE_TOOLS',
    'get_tool',
    'get_all_tools',
]

__version__ = '1.0.0'
