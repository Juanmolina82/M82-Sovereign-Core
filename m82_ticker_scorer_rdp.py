import os, sys, sqlite3
from datetime import datetime

try:
    import refinitiv.data as rd
except ImportError:
    pass

DB_PATH = os.path.expanduser('~/M82/m82_database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.execute('PRAGMA journal_mode=WAL;')
    return conn

def run_bulk_rdp_scorer():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('CREATE TABLE IF NOT EXISTS price_ticks (asset TEXT PRIMARY KEY, last_price REAL)')
    c.execute('SELECT last_price FROM price_ticks WHERE asset="US10Y"')
    row_us10y = c.fetchone()
    us10y = row_us10y[0] if row_us10y else 5.35

    drain_scale = 0.30 if us10y >= 5.30 else 0.50
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print('🏛️ [M82 BULK ENGINE] Iniciando barrido masivo...')
    print(f'📊 Macro Yield US10Y: {us10y}% | Target Scale: {drain_scale:.2f}x')

    target_universe = [
        'AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 'META', 'TSLA', 'BRK-B',
        'JPM', 'V', 'UNH', 'MA', 'PG', 'HD', 'JNJ', 'BAC', 'XOM',
        'LLY', 'AVGO', 'COST', 'AMD', 'NFLX', 'CRM', 'ORCL', 'CVX'
    ]

    # Intentar conexión con la AppKey M82_CORE_V6_STREAM
    app_key = 'e59e4b716a02411888b5510f94ef7d92f7121b1a'
    user = 'jmmp@molina82.com'
    password = 'Trader2026****'
    
    rdp_active = False
    try:
        session = rd.session.platform.Definition(
            app_key=app_key,
            grant=rd.session.platform.GrantPassword(username=user, password=password),
            signon_control=True
        ).get_session()
        
        session.open()
        if session.get_open_state() == rd.session.OpenState.Opened:
            rd.session.set_default(session)
            rdp_active = True
            print('⚡ Conexión exitosa con Refinitiv RDP (M82_CORE_V6_STREAM)')
    except Exception:
        rdp_active = False

    pending_count = 0
    skipped_count = 0

    if rdp_active:
        try:
            ric_universe = [f'{t}.O' if t in ['AAPL','MSFT','NVDA','AMZN','GOOGL','META','TSLA','AVGO','COST','AMD','NFLX'] else f'{t}.N' for t in target_universe]
            bulk_data = rd.get_data(universe=ric_universe, fields=['TR.PriceClose', 'TR.PriceClose(1D ago)', 'TR.Volume', 'TR.AvgDailyVolume30D'])
            
            for _, row in bulk_data.iterrows():
                ticker = str(row.get('Instrument', '')).split('.')[0]
                close_price = row.get('PriceClose', 0.0) or 0.0
                prev_close = row.get('PriceClose 1D ago', 0.0) or 0.0
                vol = row.get('Volume', 0.0) or 0.0
                avg_vol = row.get('AvgDailyVolume30D', 1.0) or 1.0

                if prev_close == 0: continue
                momentum = ((close_price / prev_close) - 1.0) * 100.0
                vol_spike = vol / avg_vol if avg_vol > 0 else 1.0

                base_score = 60 + (momentum * 2.5) + ((vol_spike - 1.0) * 5.0)
                final_score = int(max(0, min(100, base_score * drain_scale)))

                ev = (final_score / 100.0) * 0.85 * 2200
                status = 'PENDING' if ev >= 500 and final_score >= 60 else 'SKIPPED_LOW_EV'

                if status == 'PENDING': pending_count += 1
                else: skipped_count += 1

                headline = f'RDP Bulk Signal: {ticker} | Score: {final_score} | Mom: {momentum:.2f}%'
                clean_hl = f'rdp {ticker.lower()} score{final_score}'

                c.execute('INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, clean_headline, alpha_score, confidence, final_score, asset_impact, status, created_at, risk_budget_usd) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (f'RDP_{ticker}', headline, clean_hl, final_score, 95, final_score, ticker, status, now_str, ev * 0.10))
        except Exception as e:
            print(f'❌ Error en consulta RDP: {e}')
            rdp_active = False

    if not rdp_active:
        print('⚠️ Conmutando a extracción de alta velocidad vía Respaldo Vectorial...')
        import yfinance as yf
        for ticker in target_universe:
            try:
                t = yf.Ticker(ticker)
                hist = t.history(period='5d')
                if len(hist) < 2: continue
                
                close_price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2])
                vol = float(hist['Volume'].iloc[-1])
                avg_vol = float(hist['Volume'].mean())

                momentum = ((close_price / prev_close) - 1.0) * 100.0
                vol_spike = vol / avg_vol if avg_vol > 0 else 1.0

                base_score = 60 + (momentum * 2.5) + ((vol_spike - 1.0) * 5.0)
                final_score = int(max(0, min(100, base_score * drain_scale)))

                ev = (final_score / 100.0) * 0.85 * 2200
                status = 'PENDING' if ev >= 500 and final_score >= 60 else 'SKIPPED_LOW_EV'

                if status == 'PENDING': pending_count += 1
                else: skipped_count += 1

                headline = f'Bulk Alpha Signal: {ticker} | Score: {final_score} | Mom: {momentum:.2f}%'
                clean_hl = f'rdp {ticker.lower()} score{final_score}'

                c.execute('INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, clean_headline, alpha_score, confidence, final_score, asset_impact, status, created_at, risk_budget_usd) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (f'RDP_{ticker}', headline, clean_hl, final_score, 95, final_score, ticker, status, now_str, ev * 0.10))
            except Exception:
                continue

    conn.commit()
    print(f'🔥 [BARRIDO FINALIZADO] Registrados en DB: {pending_count} PENDING | {skipped_count} SKIPPED_LOW_EV')
    conn.close()

if __name__ == '__main__':
    run_bulk_rdp_scorer()
