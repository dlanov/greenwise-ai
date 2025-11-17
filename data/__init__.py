"""
Data processing pipeline for GreenWise AI.

Handles:
- Data ingestion from multiple sources
- Anomaly detection
- Metrics calculation
- Data quality checks
"""

from .data_ingestion import (
    DataIngestionPipeline,
    IoTDataSource,
    DatabaseSource,
    FileSource,
)
from .anomaly_detection import (
    AnomalyDetector,
    StatisticalAnomalyDetector,
    MLAnomalyDetector,
)
from .metrics_calculator import (
    MetricsCalculator,
    EnergyMetrics,
    EmissionsMetrics,
    EfficiencyMetrics,
)

__all__ = [
    # Ingestion
    'DataIngestionPipeline',
    'IoTDataSource',
    'DatabaseSource',
    'FileSource',
    # Anomaly Detection
    'AnomalyDetector',
    'StatisticalAnomalyDetector',
    'MLAnomalyDetector',
    # Metrics
    'MetricsCalculator',
    'EnergyMetrics',
    'EmissionsMetrics',
    'EfficiencyMetrics',
]

__version__ = '1.0.0'
