import curses, time
from ia_engine import Asset, fetch_world_bank_data, get_stargate_metrics

def draw_corporate_brief(stdscr):
    h, w = stdscr.getmaxyx()
    stdscr.addstr(3, 0, "--- MOLINA HOLDINGS LLC: INVESTMENT MANIFESTO ---", curses.A_BOLD)
    stdscr.addstr(5, 2, "FIRM: Hybrid Infrastructure Vehicle (Transport/Energy/Sat)", curses.color_pair(4))
    stdscr.addstr(6, 2, "CEO/PM: Juan Miguel Molina - Investment Architecture", curses.A_UNDERLINE)
    
    manifiesto = [
        "OBJECTIVE: Alpha generation via data-driven infrastructure monitoring.",
        "CORE NEEDS: Market Data (FX/FX/Cmdty) + Sovereign Risk (LatAm).",
        "USE CASE: Organize dispersed quotes into centralized visual curves.",
        "RESILIENCE: Satellite layer for monitoring physical assets.",
        "GOVERNANCE: Internal risk reporting and ESG regulatory support."
    ]
    for i, line in enumerate(manifiesto):
        if 8+i < h-2:
            stdscr.addstr(8+i, 2, f"» {line}")
    
    stdscr.addstr(15, 0, "MOLINA HOLDINGS LLC | NASHVILLE, TN | jmmp@molina82.com", curses.color_pair(1))

def draw_scenarios(stdscr):
    m = get_stargate_metrics()
    stdscr.addstr(3, 0, "--- STARGATE CORE: NODE MONITORING ---", curses.A_BOLD)
    nodos = [
        (f"  [NODE: HOKKAIDO] --> {m['Hokkaido_Node']['status']} ({m['Hokkaido_Node']['score']}/100)", 1),
        (f"  [NODE: CUA]      --> {m['Cua_Node']['status']} ({m['Cua_Node']['score']}/100)", 2),
        (f"  [GRID: ENERGY]   --> {m['Energy_Grid']['status']} ({m['Energy_Grid']['score']}/100)", 1),
        (f"  [DATA: BANK]     --> VENEZUELA: ISLA ESTADISTICA", 2)
    ]
    for i, (txt, col) in enumerate(nodos):
        stdscr.addstr(5+i, 2, txt, curses.color_pair(col))

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    stdscr.nodelay(True)
    view = "MAIN"
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.addstr(0, 0, "MOLINA AI PLATFORM | KKR CORE SYSTEM", curses.A_BOLD)
        stdscr.addstr(1, 0, "[1] DASHBOARD  [2] NODOS  [3] INVESTMENT BRIEF  [q] EXIT", curses.color_pair(4))
        
        if view == "MAIN":
            stdscr.addstr(3, 0, "MOLINA HOLDINGS: HYBRID INFRASTRUCTURE MONITOR", curses.A_BOLD)
            stdscr.addstr(5, 0, "CURRENT SCREENING:", curses.A_UNDERLINE)
            stdscr.addstr(6, 2, "ASSET: SATELLITE LAYER    | STATUS: ACTIVE", curses.color_pair(1))
            stdscr.addstr(7, 2, "ASSET: TRADITIONAL INFRA  | STATUS: MONITORING", curses.color_pair(1))
            stdscr.addstr(8, 2, "ASSET: VENEZUELA EXPOSURE | STATUS: STRESS", curses.color_pair(2))
        elif view == "SCENARIOS":
            draw_scenarios(stdscr)
        elif view == "BRIEF":
            draw_corporate_brief(stdscr)

        stdscr.addstr(h-2, 0, "AUDIT 12/12: INVESTMENT FRAMEWORK COMPLIANT | CEO: J.M. MOLINA", curses.color_pair(4))
        
        ch = stdscr.getch()
        if ch == ord('1'): view = "MAIN"
        elif ch == ord('2'): view = "SCENARIOS"
        elif ch == ord('3'): view = "BRIEF"
        elif ch == ord('q'): break
        time.sleep(0.5)

if __name__ == "__main__":
    curses.wrapper(main)
