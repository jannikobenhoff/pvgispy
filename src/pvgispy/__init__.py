"""An interface for the PVGIS Api."""

from .daily import Daily
from .hourly import Hourly
from .monthly import Monthly
from .tmy import TMY

__all__ = ["Daily", "Hourly", "TMY", "Monthly"]
