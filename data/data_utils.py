"""Data utilities for loading and transforming data."""

import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

def load_mobility_data() -> Dict[str, List[Dict]]:
    """Load mobility protocol data."""
    return {
        "Fase 1: Mobilidade Fundamental": [
            {
                "name": "Mobilidade de Quadril",
                "sets": 3,
                "reps": "10 por lado",
                "equipment": "Nenhum",
                "duration": "5 minutos",
                "notes": "Mantenha a coluna neutra durante o movimento"
            },
            {
                "name": "Mobilidade de Ombros",
                "sets": 2,
                "reps": "15 repetições",
                "equipment": "Faixa elástica",
                "duration": "4 minutos",
                "notes": "Foco na rotação escapular"
            }
        ],
        "Fase 2: Força e Estabilidade": [
            {
                "name": "Prancha com Rotação",
                "sets": 3,
                "reps": "8 por lado",
                "equipment": "Tapete",
                "duration": "6 minutos",
                "notes": "Mantenha o core engajado"
            },
            {
                "name": "Bird Dog",
                "sets": 3,
                "reps": "12 alternados",
                "equipment": "Tapete",
                "duration": "5 minutos",
                "notes": "Mantenha quadril nivelado"
            }
        ],
        "Fase 3: Integração de Movimentos": [
            {
                "name": "Flow de Yoga",
                "sets": 1,
                "reps": "Sequência completa",
                "equipment": "Tapete",
                "duration": "10 minutos",
                "notes": "Respire profundamente"
            },
            {
                "name": "Animal Flow",
                "sets": 2,
                "reps": "30 segundos cada",
                "equipment": "Nenhum",
                "duration": "8 minutos",
                "notes": "Transições suaves"
            }
        ]
    }

def load_lllt_data() -> Dict[str, List[Dict]]:
    """Load LLLT protocol data."""
    return {
        "Áreas de Tratamento": [
            {
                "name": "Região Lombar",
                "duration": "8 minutos",
                "power": "100mW",
                "wavelength": "808nm",
                "notes": "Aplicar em movimento circular"
            },
            {
                "name": "Articulação do Joelho",
                "duration": "6 minutos",
                "power": "100mW",
                "wavelength": "808nm",
                "notes": "Cobrir toda a articulação"
            }
        ]
    }

def get_progress_metrics() -> List[Dict]:
    """Return progress metrics data."""
    return [
        {
            "icon": "📈",
            "title": "Consistência do Tratamento",
            "value": "85%",
            "delta": "+5%",
            "description": "Últimos 30 dias"
        },
        {
            "icon": "✅",
            "title": "Aderência ao Protocolo",
            "value": "92%",
            "delta": "+2%",
            "description": "Esta semana"
        },
        {
            "icon": "⏱️",
            "title": "Tempo de Recuperação",
            "value": "28 min",
            "delta": "-3 min",
            "description": "Média por sessão"
        }
    ]

def get_session_history(days: int = 30) -> pd.DataFrame:
    """Generate sample session history data."""
    dates = [datetime.now() - timedelta(days=x) for x in range(days)]
    data = []
    
    for date in dates:
        if date.weekday() < 5:  # Only weekdays
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "protocol": "Mobilidade" if date.weekday() % 2 == 0 else "LLLT",
                "duration": round(25 + (date.day % 10), 1),
                "completed_exercises": 4 + (date.day % 3),
                "notes": "Sessão completa" if date.day % 5 != 0 else "Sessão parcial"
            })
    
    return pd.DataFrame(data)

def get_key_adjustments() -> List[Dict]:
    """Return key protocol adjustments data."""
    return [
        {
            "date": "2024-03-15",
            "type": "Mobilidade",
            "adjustment": "Aumentado séries de exercícios de quadril",
            "reason": "Progresso consistente"
        },
        {
            "date": "2024-03-10",
            "type": "LLLT",
            "adjustment": "Ajustado tempo de exposição",
            "reason": "Otimização do tratamento"
        }
    ] 