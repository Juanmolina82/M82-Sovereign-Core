#!/usr/bin/env python3
import os
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

DOSSIER_DIR = os.path.expanduser("~/M82/dossier")
M82_AGENT_KEY = "MOLINA82-BLINDAJE-2026-CHARALLAVE"

os.makedirs(DOSSIER_DIR, exist_ok=True)

app = FastAPI(title="MOLINA82 Private Intelligence")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

def get_dossier_context(query: str) -> str:
    matches = []
    keywords = query.lower().split()
    for file in os.listdir(DOSSIER_DIR):
        if file.endswith(".txt"):
            path = os.path.join(DOSSIER_DIR, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if any(kw in line.lower() for kw in keywords if len(kw) > 2):
                        matches.append(f"[{file}]: {line.strip()}")
                        if len(matches) >= 5:
                            break
    return "\n".join(matches) if matches else "Consulta procesada con éxito por el Nodo Local MOLINA82."

@app.post("/v1/chat")
async def chat_endpoint(req: ChatRequest, authorization: Optional[str] = Header(None)):
    if not authorization or authorization.replace("Bearer ", "") != M82_AGENT_KEY:
        raise HTTPException(status_code=401, detail="Token MOLINA82 inválido.")

    dossier = get_dossier_context(req.message)
    
    if req.message.strip() == "1":
        response_text = (
            "**[MOLINA82 - ANÁLISIS ESTRATÉGICO GEOPARK (GPRK)]**\n\n"
            "• **Valoración Operativa:** GeoPark mantiene operaciones enfocadas en eficiencia de flujo de caja y producción optimizada en la región.\n"
            "• **Factores de Riesgo:** Exposición a fluctuaciones de precios del crudo y riesgo regulatorio/geopolítico regional.\n"
            "• **Oportunidades:** Resiliencia en costos de extracción y potencial de expansión en activos maduros.\n\n"
            f"**Contexto Dossier Local:**\n{dossier}"
        )
    elif req.message.strip() == "2":
        response_text = (
            "**[MOLINA82 - EVALUACIÓN MACROECONÓMICA Y DEUDA SOBERANA]**\n\n"
            "• **Exposición de Deuda:** Monitoreo constante de reestructuración y rendimiento de bonos soberanos/PDVSA.\n"
            "• **Entorno Inflacionario:** Estabilización relativa basada en políticas de encaje y flujo de divisas.\n\n"
            f"**Contexto Dossier Local:**\n{dossier}"
        )
    elif req.message.strip() == "3":
        response_text = (
            "**[MOLINA82 - BRIEFING FAJA DEL ORINOCO]**\n\n"
            "• **Producción:** Capacidad de refinamiento y mejoramiento de crudo extrapesado.\n"
            "• **Inversión Extranjera:** Marcos de participación en joint-ventures estratégicas.\n\n"
            f"**Contexto Dossier Local:**\n{dossier}"
        )
    else:
        response_text = (
            f"**[MOLINA82 NODO CHARALLAVE]**\n\n"
            f"• **Estado:** ONLINE / OPERATIVO\n"
            f"• **Consulta:** {req.message}\n\n"
            f"**Información de Dossier:**\n{dossier}"
        )

    return {"response": response_text, "status": "ONLINE", "model_used": "M82-Autonomous-Engine"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8083)
