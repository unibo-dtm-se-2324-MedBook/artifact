from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import requests

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

@dataclass
class QueryResult:
    total_reports_considered: int
    top_reactions: List[Dict[str, Any]] # list of dictionaries with reactions
    filters_used: Dict[str, Any] # filters that were actually applied

def build_search(drug: str, filter: PatientFilters, suspect_only: bool = True) -> str:
    pass 

def fetch_risks(drug_query: str, filters: PatientFilters, top_n: int = DEFAULT_TOP_N, suspect_only: bool = True): # -> QueryResult:
    params = {
        'search': build_search(drug_query, filters, suspect_only),
        'count': 'patient.reaction.reactionmeddrapt.exact',
        'limit': max(1, top_n),
    }
    
    # GET request to API
    resp = requests.get(OPENFDA_EVENT_URL, params = params, timeout = 30) # API response timeout - 30 sec 

    if resp.status_code == 404: # If error 404 = 'no results'
        return {}
    resp.raise_for_status() # If other error -> throw exception
    
    data = resp.json()
    return data