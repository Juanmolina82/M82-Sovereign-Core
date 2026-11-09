#!/usr/bin/env python3
import json, re

class M82Agent:
    """
    Agente Autónomo de Análisis Macro, Sintaxis Quant y Evaluación Geopolítica.
    """
    def __init__(self, name="M82-AGI-Core"):
        self.name = name

    def analyze_signal(self, headline, source):
        headline_upper = headline.upper()
        
        # Algoritmo de Priorización e Impacto Cuantitativo
        high_impact_keywords = [
            "SANCTIONS", "OIL", "HORMUZ", "FED", "RATE", "WAR", "CITGO", 
            "TRUMP", "ZELENSKYY", "CHINA", "TAIWAN", "INTEREST RATES", "VENEZUELA"
        ]
        
        score = 65  # Base score
        matched_tags = []
        for kw in high_impact_keywords:
            if kw in headline_upper:
                score += 7
                matched_tags.append(kw)
        
        score = min(score, 99)

        # Matriz de Sesgo / Sentiment
        if any(w in headline_upper for w in ["CRASH", "WAR", "SANCTION", "CUT", "SELLOFF", "RISK"]):
            sentiment = "BEARISH / RISK-OFF 🔴"
        elif any(w in headline_upper for w in ["RALLY", "SURGE", "AGREEMENT", "BEAT", "GROWTH"]):
            sentiment = "BULLISH / RISK-ON 🟢"
        else:
            sentiment = "NEUTRAL / NEUTRAL-NEURAL ⚪"

        # Generación de Síntesis Ejecutiva por el Agente
        executive_summary = (
            f"El agente {self.name} ha procesado la señal procedente de {source}. "
            f"Se detecta una correlación crítica en los vectores: {', '.join(matched_tags) if matched_tags else 'MACRO_GENERIC'}. "
            f"Sesgo proyectado: {sentiment}."
        )

        return {
            "score": score,
            "sentiment": sentiment,
            "summary": executive_summary,
            "tags": matched_tags if matched_tags else ["GLOBAL_MACRO"]
        }

if __name__ == "__main__":
    agent = M82Agent()
    print(agent.analyze_signal("US Sanctions Oil Tankers near Hormuz", "M82_WIRE_FLOW_PREDICTOR"))
