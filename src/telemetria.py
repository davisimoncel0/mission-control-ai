"""Geracao de dados simulados de telemetria — Trilha EnviroSat."""
import random
from datetime import datetime


def coletar() -> dict:
    """
    Gera dados simulados de telemetria do EnviroSat-1.
    Baseado em satelite de observacao ambiental similar ao Amazonia-1 / Landsat.
    """
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sensor_termico": round(random.uniform(20.0, 85.0), 2),
        "sensor_optico_ndvi": round(random.uniform(0.0, 1.0), 3),
        "buffer_imagens_pct": round(random.uniform(10.0, 100.0), 1),
        "precisao_geo_metros": round(random.uniform(5.0, 150.0), 1),
        "energia_disponivel_pct": round(random.uniform(5.0, 100.0), 1),
    }
