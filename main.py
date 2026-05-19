import asyncio
import logging
import yfinance as yf

# Configuración del Ledger de Monitoreo M82
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [M82 BROAD-MARKET] - %(levelname)s - %(message)s'
)

# Definición de la Matriz de Cobertura de Wall Street (Fijada desde el radar M82)
SECTORES = {
    "TECNOLOGÍA & IA": ["NVDA", "TSLA", "MSFT", "AAPL"],
    "FINANCIERO & BANCA": ["JPM", "BAC"],
    "CONSUMO & DEFENSA": ["WMT", "KO", "LMT"]
}

async def analizar_sector(nombre_sector, tickers):
    logging.info(f"Procesando matriz de datos para el sector: {nombre_sector}")
    for ticker in tickers:
        try:
            # Consulta asíncrona no bloqueante mediante subprocesos de yfinance
            loop = asyncio.get_event_loop()
            t_obj = yf.Ticker(ticker)
            
            # Extraer telemetría básica (Precio spot y ratio P/E)
            info = await loop.run_in_executor(None, lambda: t_obj.info)
            price = info.get("currentPrice") or info.get("regularMarketPrice") or 0.0
            pe_ratio = info.get("trailingPE") or 0.0
            change = info.get("regularMarketChangePercent") or 0.0
            
            # Formatear salida analítica para los Deploy Logs
            pe_str = f"{pe_ratio:.2f}x" if pe_ratio else "N/A"
            logging.info(
                f"[{ticker}] Spot: ${price:.2f} USD | Var: {change:.2f}% | P/E Ratio: {pe_str}"
            )
        except Exception as e:
            logging.error(f"Error extrayendo métricas para {ticker}: {str(e)}")

async def main():
    logging.info("Inicializando clúster soberano multisectorial de Wall Street...")
    
    while True:
        # Ejecutar el análisis de todos los sectores en paralelo para máxima velocidad
        tareas = [analizar_sector(sector, tickers) for sector, tickers in SECTORES.items()]
        await asyncio.gather(*tareas)
        
        logging.info("Ciclo de captura completado. Próxima transmisión en 5 minutos...")
        # Intervalo de refresco para el monitoreo institucional continuo
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
