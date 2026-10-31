import sqlite3, os, urllib.request

DB_PATH = os.path.expanduser('~/M82/m82_database.db')
NTFY_TOPIC = 'M82-Molina-Alerts-v2'

def send_ntfy_alert(title, message, priority='high'):
    try:
        req = urllib.request.Request(
            f'https://ntfy.sh/{NTFY_TOPIC}',
            data=message.encode('utf-8'),
            headers={'Title': title, 'Priority': priority, 'Tags': 'warning,rotating_light,dollar'}
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f'Error ntfy: {e}')

def run_cascade_supervisor():
    if not os.path.exists(DB_PATH):
        print(f'DB no encontrada en {DB_PATH}')
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print('=' * 60)
    print('[DANEKA M82] EVALUANDO CASCADA GEOPOLITICA (3 CAPAS)')
    print('=' * 60)

    # 1. Capa Fisica
    c.execute("""
        SELECT daemon_source, final_score, headline, created_at 
        FROM m82_multi_stream 
        WHERE (daemon_source LIKE '%SOUTHCOM%' OR daemon_source LIKE '%MARITIME%' OR daemon_source LIKE '%CARIBBEAN%')
          AND final_score >= 85 AND date(created_at) = date('now')
        ORDER BY created_at DESC LIMIT 1;
    """)
    l1 = c.fetchone()

    # 2. Capa Regulatoria
    c.execute("""
        SELECT daemon_source, final_score, headline, created_at 
        FROM m82_multi_stream 
        WHERE (daemon_source LIKE '%OFAC%' OR daemon_source LIKE '%SANCTION%')
          AND status = 'DISPATCHED' AND final_score >= 90 AND date(created_at) = date('now')
        ORDER BY created_at DESC LIMIT 1;
    """)
    l2 = c.fetchone()

    # 3. Capa Macro
    c.execute("""
        SELECT daemon_source, final_score, headline, created_at 
        FROM m82_multi_stream 
        WHERE (daemon_source LIKE '%VE_OIL%' OR daemon_source LIKE '%CREDIT_DEFAULT%' OR daemon_source LIKE '%SWAP%')
          AND final_score >= 85 AND date(created_at) = date('now')
        ORDER BY created_at DESC LIMIT 1;
    """)
    l3 = c.fetchone()

    p1 = f"ACTIVADA ({l1[1]})" if l1 else "PASIVA (<85)"
    p2 = f"DISPATCHED ({l2[1]})" if l2 else "PASIVA"
    p3 = f"RE-PRICING ({l3[1]})" if l3 else "PASIVA"

    print(f'1. Capa Fisica (AIS/SOUTHCOM):     {p1}')
    print(f'2. Capa Regulatoria (OFAC/Lic):   {p2}')
    print(f'3. Capa Macro (VE Oil/CDS):        {p3}')

    if l1 and l2 and l3:
        send_ntfy_alert('M82 RISK EVENT - CASCADA COMPLETA (3/3)', f'FULL ALLOCATION 1.0x\n- {l1[2]}\n- {l2[2]}\n- {l3[2]}', 'max')
        print('\nTRIGGER CRITICO: Escalando Risk Governor a 1.0x.')
    elif l1 and l2:
        send_ntfy_alert('M82 RISK EVENT - FISICA + OFAC (2/3)', f'ESCALANDO A 0.60x\n- {l1[0]}: {l1[2]}\n- {l2[0]}: {l2[2]}', 'high')
        print('\nCASCADA PARCIAL (2/3): Escalando Risk Governor a 0.60x.')
    else:
        print('\nPOSTURA CONSERVADORA: Manteniendo BUNKER MODE (0.30x).')

    conn.close()

if __name__ == '__main__':
    run_cascade_supervisor()
