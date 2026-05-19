import asyncio
import logging
import yfinance as yf

# Configuración del Ledger de Monitoreo M82
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [M82 BROAD-MARKET] - %(levelname)s - %(message)s'
)

# Matriz de Cobertura de Wall Street
SECTORES = {
    "TECNOLOGÍA & IA": ["NVDA", "TSLA", "MSFT", "AAPL"],
    "FINANCIERO & BANCA": ["JPM", "BAC"],
    "CONSUMO & DEFENSA": ["WMT", "KO", "LMT"]
}

def consultar_ticker_sincrono(ticker):
    """Función aislada para interactuar limpiamente con la API de yfinance"""
    t_obj = yf.Ticker(ticker)
    info = t_obj.info
    price = info.get("currentPrice") or info.get("regularMarketPrice") or 0.0
    pe_ratio = info.get("trailingPE") or 0.0
    change = info.get("regularMarketChangePercent") or 0.0
    return price, pe_ratio, change

async def analizar_sector(nombre_sector, tickers):
    logging.info(f"Procesando matriz de datos para el sector: {nombre_sector}")
    for ticker in tickers:
        try:
            # Uso de asyncio.to_thread para evitar 'no running event loop' en Python 3.11
            price, pe_ratio, change = await asyncio.to_thread(consultar_ticker_sincrono, ticker)
            
            pe_str = f"{pe_ratio:.2f}x" if pe_ratio else "N/A"
            logging.info(
                f"[{ticker}] Spot: ${price:.2f} USD | Var: {change:.2f}% | P/E Ratio: {pe_str}"
            )
        except Exception as e:
            logging.error(f"Error extrayendo métricas para {ticker}: {str(e)}")

async def main():
    logging.info("Inicializando clúster soberano multisectorial de Wall Street...")
    
    while True:
        # Ejecución secuencial controlada por sectores para mitigar bloqueos de IP
        for sector, tickers in SECTORES.items():
            await analizar_sector(sector, tickers)
            
        logging.info("Ciclo de captura completado. Próxima transmisión en 5 minutos...")
        await asyncio.sleep(300)

if __name__ == "__main__":
    # Arrancar el ciclo maestro asegurando la existencia del loop global
    asyncio.run(main())
