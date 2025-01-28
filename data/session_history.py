"""Session history data."""

from datetime import datetime, timedelta
from typing import List, Dict, Any

def get_session_history() -> List[Dict[str, Any]]:
    """Return session history data."""
    today = datetime.now()
    return [
        {
            "date": today.strftime("%Y-%m-%d"),
            "duration": "45 minutos",
            "exercises": "6 exercícios",
            "notes": "Completou rotina matinal com forma melhorada",
            "protocol": "mobility",
            "metrics": {
                "intensidade": "Moderada",
                "qualidade": "Excelente",
                "energia": "Alta"
            }
        },
        {
            "date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
            "duration": "30 minutos",
            "exercises": "4 exercícios",
            "notes": "Foco em mobilidade de quadril",
            "protocol": "mobility",
            "metrics": {
                "intensidade": "Leve",
                "qualidade": "Boa",
                "energia": "Moderada"
            }
        },
        {
            "date": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
            "duration": "60 minutos",
            "exercises": "Protocolo completo",
            "notes": "Sessão LLLT com foco em recuperação",
            "protocol": "lllt",
            "metrics": {
                "intensidade": "Alta",
                "cobertura": "Completa",
                "resposta": "Positiva"
            }
        }
    ] 