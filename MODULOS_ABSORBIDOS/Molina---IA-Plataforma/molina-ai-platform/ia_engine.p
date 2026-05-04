# ia_engine.py
#
# Núcleo de inteligencia artificial para tu plataforma.
# Aquí irás metiendo tus algoritmos propios, modelos, reglas, etc.

from dataclasses import dataclass
from typing import List, Dict, Any
import math

# ========== MODELOS DE DATOS BÁSICOS ==========

@dataclass
class Asset:
    ticker: str
    category: str      # equity, fx, rates, credit, infra, energy, etc.
    price: float
    vol: float         # volatilidad implícita o histórica
    score: float       # tu score interno (0‑1)


@dataclass
class RiskSignal:
    name: str
    value: float
    threshold: float
    direction: str     # "UP" riesgo sube, "DOWN" baja
    weight: float      # importancia en el sistema


# ========== ALGORITMO 1: RISK ENGINE GLOBAL ==========

def compute_global_risk_index(assets: List[Asset], signals: List[RiskSignal]) -> Dict[str, Any]:
    """
    Construye un índice 0‑100 de riesgo macro usando:
    - concentración de riesgo en tus activos
    - número e intensidad de señales por encima de umbral
    """
    if not assets and not signals:
        return {"score": 0.0, "label": "NEUTRAL", "explanation": "No data."}

    # 1) riesgo de cartera por volatilidad y score
    risk_from_assets = 0.0
    total_weight = 0.0
    for a in assets:
        w = max(0.01, a.score)  # evita cero
        total_weight += w
        # riesgo marginal: vol normalizada * score
        risk_from_assets += min(1.0, a.vol / 50.0) * w

    if total_weight > 0:
        risk_from_assets /= total_weight

    # 2) riesgo de señales
    signal_risk = 0.0
    total_s_w = 0.0
    for s in signals:
        if s.threshold == 0:
            continue
        ratio = (s.value / s.threshold) if s.direction == "UP" else (s.threshold / max(1e-6, s.value))
        # ratio > 1 implica señal activa
        intensity = max(0.0, min(2.0, ratio - 1.0)) / 2.0  # 0‑1
        sw = max(0.1, s.weight)
        total_s_w += sw
        signal_risk += intensity * sw

    if total_s_w > 0:
        signal_risk /= total_s_w

    # 3) combinación no lineal
    combined = 100.0 * (0.6 * risk_from_assets + 0.4 * signal_risk)

    if combined < 25:
        label = "GREEN – RISK-ON"
    elif combined < 60:
        label = "YELLOW – MIXED"
    else:
        label = "RED – STRESS"

    explanation = (
        f"Global Risk Index {combined:0.1f}/100 "
        f"(assets={risk_from_assets:0.2f}, signals={signal_risk:0.2f})."
    )

    return {
        "score": round(combined, 1),
        "label": label,
        "assets_component": round(risk_from_assets, 3),
        "signals_component": round(signal_risk, 3),
        "explanation": explanation,
    }


# ========== ALGORITMO 2: SCORING DE PROYECTOS DE INFRA / DATA CENTERS ==========

@dataclass
class InfraProject:
    name: str
    capex_bn: float     # capex en miles de millones
    gw_power: float     # capacidad eléctrica (GW)
    chips_k: float      # nº de chips en miles
    country_risk: float # 0‑1 (1 = riesgo alto)
    regulatory_score: float # 0‑1 (1 = marco muy favorable)
    energy_mix_green: float # 0‑1 fracción renovable


def score_infra_ai(project: InfraProject) -> Dict[str, Any]:
    """
    Puntúa proyectos tipo Stargate (0‑100) para ranking interno.
    """
    # escala de tamaño
    scale = min(1.0, project.capex_bn / 100.0)  # 100bn+ se considera 1
    power_scale = min(1.0, project.gw_power / 1.0)
    chips_scale = min(1.0, project.chips_k / 400.0)  # 400k chips = 1.0

    size_component = 0.4 * scale + 0.3 * power_scale + 0.3 * chips_scale

    # riesgo / regulación / verde
    risk_component = 1.0 - project.country_risk
    policy_component = project.regulatory_score
    green_component = project.energy_mix_green

    raw = (
        0.4 * size_component
        + 0.25 * risk_component
        + 0.2 * policy_component
        + 0.15 * green_component
    )

    score = 100.0 * raw

    if score >= 80:
        bucket = "FLAGSHIP AI HUB"
    elif score >= 60:
        bucket = "STRONG PLATFORM"
    elif score >= 40:
        bucket = "OPTIONALITY PLAY"
    else:
        bucket = "SPECULATIVE"

    return {
        "score": round(score, 1),
        "bucket": bucket,
        "size_component": round(size_component, 3),
        "risk_component": round(risk_component, 3),
        "policy_component": round(policy_component, 3),
        "green_component": round(green_component, 3),
    }


# ========== ALGORITMO 3: RESUMIDOR SIMPLE DE NOTICIAS (SIN API EXTERNA) ==========

def simple_news_summary(text: str, max_len: int = 280) -> str:
    """
    Recorta y limpia un bloque de texto para tu ticker,
    sin depender de ningún modelo externo.
    """
    clean = " ".join(text.strip().split())
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 3] + "..."
