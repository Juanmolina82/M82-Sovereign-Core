import asyncio
import logging
import yfinance as yf

# Configuración de la Consola M82 con formato de auditoría financiera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [M82 BROAD-MARKET] - %(levelname)s - %(message)s'
)

# Matriz Multisectorial de Cobertura
SECTORES = {
    "TECNOLOGÍA & IA": ["NVDA", "TSLA", "MSFT", "AAPL"],
    "FINANCIERO & BANCA": ["JPM", "BAC"],
    "CONSUMO & DEFENSA": ["WMT", "KO", "LMT"]
}

# Umbral crítico de volatilidad para el bloque de ganancias (5.0%)
UMBRAL_VOLATILIDAD = 5.0

def consultar_ticker_seguro(ticker):
    """Extrae métricas operacionales usando canales históricos resilients"""
    t_obj = yf.Ticker(ticker)
    
    # Canal de precio de alta disponibilidad
    hist = t_obj.history(period="1d")
    if not hist.empty:
        price = float(hist['Close'].iloc[-1])
        open_p = float(hist['Open'].iloc[-1])
        change = ((price - open_p) / open_p) * 100 if open_p else 0.0
    else:
        price, change = 0.0, 0.0

    # Canal secundario para la extracción segura del ratio P/E
    try:
        info = t_obj.info
        pe_ratio = info.get("trailingPE") or info.get("forwardPE") or 0.0
    except Exception:
        pe_ratio = 0.0

    return price, pe_ratio, change

async def analizar_sector(nombre_sector, tickers):
    logging.info(f"Abriendo canal de datos sectorial: {nombre_sector}")
    for ticker in tickers:
        try:
            # Consulta delegada al gestor de hilos de Linux
            price, pe_ratio, change = await asyncio.to_thread(consultar_ticker_seguro, ticker)
            
            if price > 0:
                pe_str = f"{pe_ratio:.2f}x" if pe_ratio else "N/A"
                
                # --- CONTROLADOR DE ALERTAS DE VOLATILIDAD M82 ---
                if abs(change) >= UMBRAL_VOLATILIDAD:
                    logging.warning(
                        f"🚨 [ALERTA MAXIMA M82] - {ticker} REGISTRA MOVIMIENTO EXTREMO: {change:.2f}% | Spot: ${price:.2f} USD | P/E: {pe_str}"
                    )
                else:
                    logging.info(
                        f"[{ticker}] Spot: ${price:.2f} USD | Var: {change:.2f}% | P/E: {pe_str}"
                    )
            else:
                logging.warning(f"[{ticker}] Alerta: Proveedor de datos devolvió búfer vacío.")
                
            # Retraso táctico anti-bloqueo entre peticiones
            await asyncio.sleep(3)
            
        except Exception as e:
            logging.error(f"Fallo en módulo de transmisión para {ticker}: {str(e)}")

async def main():
    logging.info("Inicializando clúster soberano multisectorial de Wall Street...")
    
    while True:
        for sector, tickers in SECTORES.items():
            await analizar_sector(sector, tickers)
            await asyncio.sleep(5)
            
        logging.info("Matriz analizada por completo. Entrando en reposo por 5 minutos...")
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
