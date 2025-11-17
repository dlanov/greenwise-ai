"""
Utility functions and helpers for GreenWise AI.

Provides:
- Logging configuration
- Input validation
- Data transformation helpers
- Common utilities
"""

from .logging_config import (
    setup_logging,
    get_logger,
    log_execution_time,
)
from .validators import (
    validate_energy_data,
    validate_emissions_data,
    validate_recommendation,
    ValidationError,
)
from .helpers import (
    format_number,
    format_percentage,
    calculate_savings,
    generate_report_id,
    sanitize_input,
)

__all__ = [
    # Logging
    'setup_logging',
    'get_logger',
    'log_execution_time',
    # Validation
    'validate_energy_data',
    'validate_emissions_data',
    'validate_recommendation',
    'ValidationError',
    # Helpers
    'format_number',
    'format_percentage',
    'calculate_savings',
    'generate_report_id',
    'sanitize_input',
]

__version__ = '1.0.0'
