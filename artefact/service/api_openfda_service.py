from dataclasses import dataclass
from typing import Optional

OPENFDA_EVENT_URL = 'https://api.fda.gov/drug/event.json'
AGE_UNIT_YEARS = 801
DEFAULT_TOP_N = 6

@dataclass
class PatientFilters:
    gender: Optional[int] = None
    age: Optional[float] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    country: Optional[str] = None

    age_window: float = 0.0
    weight_window_pct: float = 0.0
    height_window_pct: float = 0.0     