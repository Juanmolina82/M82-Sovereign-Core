#!/usr/bin/env python3
import os, json
import refinitiv.data as rd

# Se puede definir APP_KEY vía variable de entorno o sesión local de M82 Wire Workspace
M82_WIRE_APP_KEY = os.getenv("M82_WIRE_APP_KEY", "DEFAULT_M82_APP_KEY")

def get_refinitiv_data(ric_code):
    try:
        rd.open_session()
        # Capturar campos clave: Precio actual, Cierre previo, Cambio %, Volumen
        df = rd.get_data(
            universe=[ric_code],
            fields=['CF_LAST', 'CF_CLOSE', 'NETCHNG_1', 'PCTCHNG', 'CF_VOLUME']
        )
        rd.close_session()
        
        last = df['CF_LAST'].iloc[0]
        close = df['CF_CLOSE'].iloc[0]
        change = df['NETCHNG_1'].iloc[0]
        pct = df['PCTCHNG'].iloc[0]
        
        return {
            "ric": ric_code,
            "price": float(last),
            "close": float(close),
            "change": float(change),
            "pct_change": float(pct),
            "source": "M82_WIRE_WORKSPACE"
        }
    except Exception as e:
        return {"error": str(e), "source": "M82_WIRE_WORKSPACE"}

if __name__ == "__main__":
    import sys
    ric = sys.argv[1] if len(sys.argv) > 1 else "NVDA.O"
    print(json.dumps(get_refinitiv_data(ric), indent=2))
