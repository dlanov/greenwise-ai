"""
User interface components for GreenWise AI.

Gradio-based dashboard with:
- Real-time metrics display
- Recommendation viewer
- Feedback collection
- Historical analysis
- Charts and visualizations
"""

from .dashboard import create_dashboard, DashboardComponents
from .recommendations import RecommendationsPanel, format_recommendation
from .charts import (
    create_energy_chart,
    create_emissions_chart,
    create_efficiency_chart,
    create_trend_chart,
)
from .feedback_handler import FeedbackHandler, FeedbackType

__all__ = [
    # Dashboard
    'create_dashboard',
    'DashboardComponents',
    # Recommendations
    'RecommendationsPanel',
    'format_recommendation',
    # Charts
    'create_energy_chart',
    'create_emissions_chart',
    'create_efficiency_chart',
    'create_trend_chart',
    # Feedback
    'FeedbackHandler',
    'FeedbackType',
]

__version__ = '1.0.0'
