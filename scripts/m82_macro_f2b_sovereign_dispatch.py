#!/usr/bin/env python3
import os, sys, json, sqlite3, hashlib, datetime, urllib.error, urllib.parse, urllib.request
import math
def to_float_safe(val):
    if val is None:
        return None
    try:
        import pandas as _pd
        if _pd.isna(val):
            return None
    except Exception:
        pass
    try:
        f = float(val)
        return None if (math.isnan(f) or math.isinf(f)) else f
    except Exception:
        return None


BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
JSON_PATH = os.path.join(DOCS_DIR, "M82_MASTER_KNOWLEDGE_INDEX.json")
MD_PATH = os.path.join(DOCS_DIR, "M82_MACRO_DOSSIER_MASTER_V605.md")

RICS = {
    "VE033522481=": "VENZ 13.625% 2018",
    "VE008814957=": "VENZ 7.00% 2018",
    "VE020420066=": "VENZ 7.75% 2019",
    "VE023978488=": "VENZ 6.00% 2020",
    "VE036281911=": "VENZ 12.75% 2022",
    "VE036281920=": "VENZ 9.00% 2023",
    "VE036281938=": "VENZ 8.25% 2024",
    "VE022372191=": "VENZ 7.65% 2025",
    "VE036281946=": "VENZ 11.75% 2026",
    "VE003497885=": "VENZ 9.25% 2027",
    "VE036281954=": "VENZ 9.25% 2028",
    "VE036281962=": "VENZ 11.95% 2031",
    "VENZ34":       "VENZ 9.375% 2034",
    "VE010402843=": "VENZ 9.375% 2034 ISIN",
    "VE033522473=": "VENZ 7.00% 2038",
    "VE042460214=": "VENZ Live RIC A",
    "VE036133678=": "VENZ Live RIC B",
    "VE058485153=": "VENZ Live RIC C",
    "VE048265414=": "VENZ Live RIC D",
    "USP97475AQ30=": "VENZ Live RIC E",
    "XS029436410=": "PDVSA 5.25% 2017",
    "XS046054679=": "PDVSA 8.50% 2020",
    "XS061889919=": "PDVSA 9.00% 2021",
    "XS058756451=": "PDVSA 12.75% 2022",
    "XS097523453=": "PDVSA 6.00% 2024",
    "PDVSA26":      "PDVSA 6.00% 2026",
    "XS097523461=": "PDVSA 6.00% 2026 ISIN",
    "XS029436495=": "PDVSA 5.375% 2027",
    "XS083651823=": "PDVSA 9.75% 2035",
    "XS029436720=": "PDVSA 5.50% 2037",
    "716558AC5=":   "PDVSA Live RIC A",
    "VE0919352815=": "PDVSA Live RIC B",
    "VE097527910=": "PDVSA Live RIC C",
    "716558AD3=":   "PDVSA Live RIC D",
    "716558AF8=":   "PDVSA Live RIC E",
    "VE0197837462=": "PDVSA Live RIC F",
    "VE078711887=": "PDVSA Live RIC G",
    "VE029436720=": "PDVSA 5.50% 2037 Alt",
    "VE029436495=": "PDVSA 5.375% 2027 Alt"
}

def load_local_envs():
    os.chdir(BASE_DIR)
    for fname in [".lseg_sovereign.env", ".env.refinitiv", ".env"]:
        fpath = os.path.join(BASE_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    s = line.strip()
                    if "=" in s and not s.startswith("#"):
                        k, v = s.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip().strip("\"'"))

def fetch_bonds_and_store(conn, now_iso):
    df, eng, err_msg = None, "none", ""
    fields = ["DSPLY_NAME", "BID", "ASK", "TRDPRC_1", "PRIMACT_1", "NETCHNG_1"]
    ric_list = list(RICS.keys())
    try:
        import lseg.data as ld
        ld.open_session()
        df = ld.get_data(ric_list, fields)
        ld.close_session()
        eng = "lseg.data"
    except Exception as e1:
        try:
            import refinitiv.data as rd
            rd.open_session()
            df = rd.get_data(ric_list, fields)
            rd.close_session()
            eng = "refinitiv.data"
        except Exception as e2:
            err_msg = f"{e1} | {e2}"

    lines = [f"{'RIC':<14} | {'BONO':<21} | {'BID':>6} | {'ASK':>6} | {'MID':>6} | {'CHG':>6}"]
    lines.append("-" * 74)
    valid_count = 0

    if df is not None:
        for _, r in df.iterrows():
            ric = str(r.get("Instrument", "")).strip()
            b, a = r.get("BID"), r.get("ASK")
            p = r.get("TRDPRC_1") if r.get("TRDPRC_1") is not None else r.get("PRIMACT_1")
            c = r.get("NETCHNG_1")
            bf = to_float_safe(b)
            af = to_float_safe(a)
            pf = to_float_safe(p)
            cf = to_float_safe(c)
            mid = round((bf + af) / 2, 4) if (bf is not None and af is not None) else (round(pf, 4) if pf is not None else None)
            if mid is not None:
                valid_count += 1
                t_cols = {r[1] for r in conn.execute("PRAGMA table_info(price_ticks)").fetchall()}
                if not t_cols:
                    conn.execute(
                        "CREATE TABLE IF NOT EXISTS price_ticks (id INTEGER PRIMARY KEY AUTOINCREMENT, ric TEXT, symbol TEXT, price REAL, mid REAL, bid REAL, ask REAL, source TEXT, ts TEXT)"
                    )
                    t_cols = {r[1] for r in conn.execute("PRAGMA table_info(price_ticks)").fetchall()}
                tick_map = {
                    "ric": ric,
                    "symbol": ric,
                    "instrument": ric,
                    "price": mid,
                    "mid": mid,
                    "last_px": mid,
                    "bid": bf if bf is not None else mid,
                    "ask": af if af is not None else mid,
                    "source": f"LSEG_{eng}_VZLA",
                    "ts": now_iso,
                    "ts_utc": now_iso,
                    "timestamp": now_iso,
                }
                use_cols = [c for c in tick_map if c in t_cols]
                if use_cols:
                    conn.execute(
                        f"INSERT INTO price_ticks ({', '.join(use_cols)}) VALUES ({', '.join(['?']*len(use_cols))})",
                        [tick_map[c] for c in use_cols]
                    )
            bs = f"{bf:.2f}" if bf is not None else " N/A "
            as_ = f"{af:.2f}" if af is not None else " N/A "
            ms = f"{mid:.2f}" if mid is not None else " N/A "
            cs = f"{cf:+.2f}" if cf is not None else " N/A "
            lines.append(f"{ric:<14} | {RICS.get(ric, ric)[:21]:<21} | {bs:>6} | {as_:>6} | {ms:>6} | {cs:>6}")
    else:
        lines.append(f"Sesion LSEG sin datos ({err_msg[:90]})")

    return eng, valid_count, "\n".join(lines)

def persist_macro_and_index(conn, now_iso, eng, valid_count):
    tag = "v60.5-LSEG-MACRO-F2B-VZLA-BONDS-20261128"
    headline = (
        f"Macro M82 ({eng}, ticks={valid_count}): LSEG AlphaDesk OMS/PMS nube, Wall Street F2B "
        f"y bonos VENZ/PDVSA (OFAC GL 5AA 18-Dic-2026) bajo BUNKER MODE 0.30x LOCK"
    )
    meta_obj = {
        "date_utc": now_iso,
        "node": "CHARALLAVE-L4L5-EDGE",
        "hq": "CARACAS-HQ-CENTRAL",
        "governance": {
            "mode": "BUNKER_MODE_CUSTODIA_PASIVA_030X_LOCK",
            "lockout": "NO_TRADE",
            "exposure": 0.22,
            "lock_cap": 0.30,
            "dry_powder_pct": 78.0,
            "var_daily_pct": 1.68,
            "warsh_spread_bps": 102.0
        },
        "lseg_stack": ["Workspace", "AlphaDesk", "TORA", "Autex_Trade_Route", "Autex_IOI", "REDI", "FXall", "FX_Matching", "Tradeweb", "MarketAxess"],
        "atr_scale": {"buy_side_firms": 1000, "brokers_venues": 600, "daily_equity_shares_bn": 4.0},
        "bonds_engine": eng,
        "valid_bond_ticks": valid_count,
        "ofac_gl_5aa_deadline": "2026-12-18"
    }
    meta_json = json.dumps(meta_obj, ensure_ascii=False)
    payload_hash = hashlib.sha256(f"{tag}|{headline}|{meta_json}".encode("utf-8")).hexdigest()

    cur = conn.cursor()
    cols = {r[1] for r in cur.execute("PRAGMA table_info(macro_dossier)").fetchall()}
    if "m82_tag" in cols:
        cur.execute("DELETE FROM macro_dossier WHERE m82_tag = ?", (tag,))

    val_map = {
        "source": "M82_MACRO_F2B_SOVEREIGN",
        "category": "MACRO_F2B_BONDS_DISPATCH",
        "headline": headline,
        "risk_score": 1.68,
        "m82_tag": tag,
        "sentiment": 0.86,
        "metadata_json": meta_json,
        "alpha_score": 0.88,
        "msi_index": 1875.0,
        "hash_sha256": payload_hash,
        "validated": 1,
    }
    ins_cols = [c for c in val_map if c in cols]
    cur.execute(
        f"INSERT INTO macro_dossier ({', '.join(ins_cols)}) VALUES ({', '.join(['?']*len(ins_cols))})",
        [val_map[c] for c in ins_cols]
    )
    rec_id = cur.lastrowid

    seal_cols = [r[1] for r in cur.execute("PRAGMA table_info(m82_ledger_seals_v2)").fetchall()]
    if seal_cols and rec_id:
        prev_row = cur.execute("SELECT rowid, * FROM m82_ledger_seals_v2 ORDER BY rowid DESC LIMIT 1").fetchone()
        prev_cols = [d[0] for d in cur.description] if prev_row else []
        prev_dict = dict(zip(prev_cols, prev_row)) if prev_row else {}
        prev_hash = prev_dict.get("payload_hash") or prev_dict.get("seal_hash") or ("0" * 64)
        s_map = {
            "prev_hash": prev_hash,
            "record_id": rec_id,
            "operation": "SEAL",
            "seal_type": "SEAL",
            "event_type": "SEAL",
            "payload_hash": payload_hash,
            "seal_hash": payload_hash,
            "timestamp": now_iso,
            "ts_utc": now_iso,
            "created_at": now_iso,
            "node_id": "CHARALLAVE-L4L5-EDGE",
            "node_source": "CHARALLAVE-L4L5-EDGE",
        }
        s_cols = [c for c in seal_cols if c in s_map and c not in ("seal_id", "id")]
        if s_cols:
            cur.execute(
                f"INSERT INTO m82_ledger_seals_v2 ({', '.join(s_cols)}) VALUES ({', '.join(['?']*len(s_cols))})",
                [s_map[c] for c in s_cols]
            )

    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")

    vectors = [dict(r) for r in cur.execute("SELECT * FROM macro_dossier ORDER BY rowid ASC").fetchall()]
    raw_seals = [dict(r) for r in cur.execute("SELECT * FROM m82_ledger_seals_v2 ORDER BY rowid ASC").fetchall()]

    seals = []
    for idx, s in enumerate(raw_seals, start=1):
        item = dict(s)
        sid = item.get("seal_id") if item.get("seal_id") is not None else item.get("id")
        item["seal_id_resolved"] = sid if sid is not None else idx
        item["prev_hash"] = item.get("prev_hash") or ""
        item["payload_hash"] = item.get("payload_hash") or item.get("seal_hash") or ""
        seals.append(item)

    md_sha256 = hashlib.sha256(open(MD_PATH, "rb").read()).hexdigest() if os.path.exists(MD_PATH) else None
    latest_seal = seals[-1] if seals else {}
    master_index = {
        "system": "M82_SOVEREIGN_CORE",
        "version": "v60.5",
        "workspace_user": "jmmp@molina82.com",
        "origin_topology": "CHARALLAVE-L4L5-EDGE <-> CARACAS-HQ-CENTRAL",
        "generated_at_utc": now_iso,
        "latest_tag": tag,
        "governance_state": {
            "mode": "BUNKER_MODE_CUSTODIA_PASIVA_030X_LOCK",
            "lockout": "NO_TRADE",
            "active_exposure_nav": 0.22,
            "max_exposure_cap": 0.30,
            "dry_powder_pct": 78.0,
            "daily_var_pct": 1.68,
            "warsh_spread_bps": 102.0,
            "ofac_gl_5aa_deadline": "2026-12-18"
        },
        "artifacts": {
            "macro_script": os.path.abspath(__file__),
            "master_dossier_md": MD_PATH,
            "master_dossier_sha256": md_sha256,
            "sqlite_db": DB_PATH
        },
        "ledger_integrity": {
            "total_vectors": len(vectors),
            "total_seals": len(seals),
            "latest_seal_id": latest_seal.get("seal_id_resolved"),
            "latest_payload_hash": latest_seal.get("payload_hash") or None
        },
        "cryptographic_seals": seals,
        "macro_vectors": vectors
    }
    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(master_index, f, indent=2, ensure_ascii=False)
    json_sha256 = hashlib.sha256(open(JSON_PATH, "rb").read()).hexdigest()
    return rec_id, tag, len(vectors), len(seals), json_sha256

def dispatch_channels(msg):
    bot_token = os.environ.get("M82_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("M82_PRIVATE_CHAT_ID", "").strip()
    ntfy_url = os.environ.get("M82_NTFY_URL", "").strip()
    ntfy_token = os.environ.get("M82_NTFY_TOKEN", "").strip()

    if bot_token and chat_id:
        tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": chat_id, "text": msg[:4000]}).encode("utf-8")
        req = urllib.request.Request(tg_url, data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                print("PRIVATE_BOT_HTTP:", r.status)
        except urllib.error.HTTPError as e:
            print(f"PRIVATE_BOT_HTTP_ERR: {e.code} {e.reason} | BODY: {e.read().decode('utf-8', errors='replace')}")
    else:
        print("PRIVATE_BOT_SKIPPED: defina M82_BOT_TOKEN y M82_PRIVATE_CHAT_ID en ~/.m82_env")

    if ntfy_url:
        headers = {
            "Title": "M82 Macro F2B + Wall Street + VENZ/PDVSA",
            "Priority": "high",
            "Tags": "briefcase,bank,shield",
        }
        if ntfy_token:
            headers["Authorization"] = f"Bearer {ntfy_token}"
        req_ntfy = urllib.request.Request(ntfy_url, data=msg.encode("utf-8"), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req_ntfy, timeout=15) as r2:
                print("NTFY_HTTP:", r2.status, "| URL:", ntfy_url)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            print(f"NTFY_HTTP_ERR: {e.code} {e.reason} | URL: {ntfy_url} | BODY: {err_body}")
    else:
        print("NTFY_SKIPPED: defina M82_NTFY_URL o M82_NTFY_TOPIC en ~/.m82_env")

def main():
    no_send = "--no-send" in sys.argv
    load_local_envs()
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    try:
        eng, valid_count, bond_table = fetch_bonds_and_store(conn, now_iso)
        rec_id, tag, n_vec, n_seal, json_sha = persist_macro_and_index(conn, now_iso, eng, valid_count)
    finally:
        conn.close()

    print(f"[OK] Script maestro instalado: {os.path.abspath(__file__)}")
    print(f"[OK] Vector sellado en WAL: rec_id={rec_id} | tag={tag} | vectors={n_vec} | seals={n_seal}")
    print(f"[OK] JSON SHA-256: {json_sha}")
    print(f"[OK] Bonos ({eng}) ticks={valid_count} | {now_iso}")

    msg = f"""M82 MACRO F2B + WALL STREET + VENZ/PDVSA
Nodo: Charallave L4/L5 Edge x Caracas HQ Central
Gob: BUNKER MODE 0.30x LOCK | LOCKOUT: NO TRADE
Cartera: 0.22x NAV | Dry Powder 78.0% | VaR ~1.68% | Warsh ~102.0 bps

1. LSEG AlphaDesk, TORA & Autex Trade Route (F2B): OMS/PMS nube (rebalanceo, P&L +100 campos, Shadow NAV, contabilidad, riesgo, 40 Act/UCITS/MiFID II), TORA OEMS (FIX/WebSocket APIs, spread/relative-value, pre/post-trade TCA, FXall/FX Matching, Tradeweb/MarketAxess, Digital Assets) y ATR (+1,000 buy-side, +600 brokers, +4B shares/dia, Autex IOI & REDI).
1b. Venues & Liquidez: FXall (spot/swaps/forwards/NDFs & hedging), FX Matching (profundidad/orderbook FX), Tradeweb (RFQ & curvas tasas/renta fija), MarketAxess (RFQ & liquidez credito) y Autex IOI (IOIs & anuncios pre-trade).
2. Wall Street: Equities/IA, US 10Y/Fed, USD/JPY, Brent/WTI (Ormuz/OPEP+), XAU y BTC.
3. VENZ & PDVSA ({eng}, ticks={valid_count}): Marco $237.5B y OFAC GL 5AA (18-Dic-2026).
{bond_table[:1800]}"""

    if not no_send:
        dispatch_channels(msg)

if __name__ == "__main__":
    main()
