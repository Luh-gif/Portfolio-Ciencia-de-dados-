import json
import logging
from typing import Dict, List, Any

# Configurando o logger executivo
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DataScienceFactory')

def parse_json_column(val: Any) -> Any:
    """Faz o parse seguro de uma string representando um JSON."""
    if not isinstance(val, str) or not val.strip():
        return None
    try:
        return json.loads(val)
    except json.JSONDecodeError:
        return None

def extract_amenities_features(amenities_list: List[str]) -> Dict[str, Any]:
    """Extrai features binárias relevantes de uma lista de amenidades."""
    if not amenities_list or not isinstance(amenities_list, list):
        return {
            'total_amenities': 0,
            'has_car_wash': False,
            'has_customer_toilets': False,
            'has_ev_charging': False
        }
    
    amenities_lower = [str(a).lower() for a in amenities_list]
    
    return {
        'total_amenities': len(amenities_list),
        'has_car_wash': any('car_wash' in a for a in amenities_lower),
        'has_customer_toilets': any('toilet' in a in a for a in amenities_lower),
        'has_ev_charging': any('charging' in a or 'ev' in a for a in amenities_lower),
    }

def extract_fuel_features(fuels_list: List[str]) -> Dict[str, Any]:
    """Extrai infraestrutura de combustível."""
    if not fuels_list or not isinstance(fuels_list, list):
        return {
            'total_fuel_types': 0,
            'has_premium_fuel': False
        }
    
    fuels_lower = [str(f).lower() for f in fuels_list]
    
    return {
        'total_fuel_types': len(fuels_list),
        'has_premium_fuel': any('premium' in f for f in fuels_lower)
    }

def is_station_24_hours(opening_dict: Dict[str, Any]) -> bool:
    """Através do dicionário JSON, define se o posto opera 24h."""
    if not opening_dict or not isinstance(opening_dict, dict):
        return False
    
    # Avaliamos os "usual_days"
    usual_days = opening_dict.get('usual_days', {})
    if not usual_days:
        return False
        
    # Consideramos 24h se pelomenos a maioria dos dias for 24h
    days_24h = sum(1 for day_info in usual_days.values() if isinstance(day_info, dict) and day_info.get('is_24_hours') is True)
    return days_24h >= 4

def clean_boolean_columns(val: Any) -> bool:
    """Garante que a coluna booleana retorna False quando vazia ou inválida."""
    val_str = str(val).strip().lower()
    if val_str in ['true', '1', 'yes', 't', 'y']:
        return True
    return False
