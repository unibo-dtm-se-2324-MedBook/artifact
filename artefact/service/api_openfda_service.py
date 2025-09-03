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

def create_range(value, abs_window = 0.0, pers_window = 0.0) -> str:
    if abs_window and abs_window > 0:
        low = max(0, value - abs_window)
        high = value + abs_window
        return f'[{str(int(low))}+TO+{str(int(high))}]'
    
    if pers_window and pers_window > 0:
        delta = value * pers_window
        low = max(0, value - delta)
        high = value + delta
        return f'[{str(int(low))}+TO+{str(int(high))}]'
    return str(int(value))

def build_search(drug: str, filter: PatientFilters, suspect_only: bool = True) -> str:
    drug_query = drug.replace('"', '\\"').strip()
    
    parts = []
    parts.append('(' + ' OR '.join([
        f'patient.drug.medicinalproduct:"{drug_query}"',
        f'patient.drug.openfda.brand_name:"{drug_query}"',
        f'patient.drug.openfda.substance_name:"{drug_query}"',
    ]) + ')')

    if suspect_only:
        parts.append('patient.drug.drugcharacterization:1')
    if filter.gender is not None:
        parts.append(f'patient.patientsex:{int(filter.gender)}')
    if filter.age is not None:
        parts.append(f'patient.patientonsetageunit:{AGE_UNIT_YEARS}')
        parts.append(f'patient.patientonsetage:{create_range(filter.age, abs_window = filter.age_window)}')
    if filter.weight is not None:
        parts.append(f'patient.patientweight:{create_range(filter.weight, pers_window = filter.weight_window_pct)}')
    if filter.height is not None:
        parts.append(f'patient.patientheight:{create_range(filter.height, pers_window = filter.height_window_pct)}')
    if filter.country:
        parts.append(f'occurcountry:{filter.country}')

    return "+AND+".join(parts)  

def fetch_risks(drug_query: str, filters: PatientFilters, top_n: int = DEFAULT_TOP_N, suspect_only: bool = True): # -> QueryResult:
    params = {
        'search': build_search(drug_query, filters, suspect_only),
        'count': 'patient.reaction.reactionmeddrapt.exact',
        'limit': max(1, top_n),
    }
    
    # GET request to API
    try:
        resp = requests.get(OPENFDA_EVENT_URL, params = params, timeout = 30) # API response timeout - 30 sec 
        
        if resp.status_code == 404:
            print('Error 404 detected no results')
            return {
                'error': 'No results found.',
                'status': 404,
                'kind': 'no_results'
            }      

        if resp.status_code == 405:
            print('Error 405 - error on the API side')
            return {
                'error': 'External API error, please try again later.',
                'status': 405,
                'kind': 'api_error'
            }

        if resp.status_code == 429:
            print('Error 429 - Request limit exceeded')
            return {
                'error': 'Too many requests, please slow down.',
                'status': 429,
                'kind': 'rate_limit'
            }

        if resp.status_code >= 500:
            print(f'Error {resp.status_code} - server API error')
            return {
                'error': 'API server error, please try again later.',
                'status': resp.status_code,
                'kind': 'server_error'
            }

        resp.raise_for_status() # If other error -> throw exception
        
        data = resp.json()
        return data
    
    except requests.exceptions.RequestException as ex:
        print(f'Network/API error: {ex}')
        return {
            'error': 'Network or API error, please check your connection.',
            'status': None,
            'kind': 'network_error'
        }