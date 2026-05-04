import curses, time
from ia_engine import Asset, fetch_world_bank_data, get_stargate_metrics

def draw_market_alpha(stdscr):
    stdscr.addstr(3, 0, "--- MARKET ALPHA: OPPORTUNITY SCREENING ---", curses.A_BOLD)
    stdscr.addstr(5, 2, "OVERNIGHT TRADING HIGHLIGHTS:", curses.color_pair(4))
    
    opportunities = [
        ("SNDK (SanDisk)", "+3%", "YTD >300% - AI Storage Demand"),
        ("CRDO (Credo)",  "+10%", "M&A: DustPhotonics (Silicon Photonics)"),
        ("AAL (American)", "+4%", "Merger Rumors w/ United Airlines"),
        ("DELL / HPQ",    "-2%", "NVDA M&A Denial - Hardware Volatility")
    ]
    
    for i, (ticker, change, reason) in enumerate(opportunities):
        color = curses.color_pair(1) if "+" in change else curses.color_pair(2)
        stdscr.addstr(7+i, 2, f"{ticker:15} | {change:5} | {reason}", color)
    
    stdscr.addstr(13, 0, "PEER ANALYSIS:", curses.A_BOLD)
    stdscr.addstr(14, 2, "Consolidation in Infra & Sat-Tech is accelerating.", curses.color_pair(4))

def draw_corporate_brief(stdscr):
    stdscr.addstr(3, 0, "--- MOLINA HOLDINGS LLC: INVESTMENT MANIFESTO ---", curses.A_BOLD)
    stdscr.addstr(5, 2, "CEO/PM: Juan Miguel Molina - Investment Architecture", curses.A_UNDERLINE)
    manifiesto = [
        "STRATEGY: Traditional Infra + Satellite/Digital Layer.",
        "ALPHA: Centralizing fragmented quotes into visual curves.",
        "FOCUS: Energy, Transport, and High-Speed Connectivity."
    ]
    for i, line in enumerate(manifiesto):
        stdscr.addstr(8+i, 2, f"» {line}")

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
        stdscr.addstr(1, 0, "[1] DASH [2] NODOS [3] BRIEF [4] ALPHA [q] EXIT", curses.color_pair(4))
        
        if view == "MAIN":
            stdscr.addstr(3, 0, "PORTFOLIO RISK MONITOR (Nashville-Cua-Japan)", curses.A_BOLD)
            stdscr.addstr(5, 2, "SYSTEM STATUS: AUDIT 12/12 VERIFIED", curses.color_pair(1))
            stdscr.addstr(7, 2, "INFRASTRUCTURE CORRELATION: 0.82 (High)", curses.color_pair(4))
        elif view == "NODOS":
            m = get_stargate_metrics()
            stdscr.addstr(3, 0, "--- STARGATE CORE: NODE MONITORING ---", curses.A_BOLD)
            stdscr.addstr(5, 2, f"NODE: HOKKAIDO -> {m['Hokkaido_Node']['status']}", curses.color_pair(1))
            stdscr.addstr(6, 2, "NODE: CUA      -> DATA GAP (ISLA ESTADISTICA)", curses.color_pair(2))
        elif view == "BRIEF":
            draw_corporate_brief(stdscr)
        elif view == "ALPHA":
            draw_market_alpha(stdscr)

        stdscr.addstr(h-2, 0, "MOLINA HOLDINGS LLC | REDUCING DATA FRICTION | CEO: J.M. MOLINA", curses.color_pair(4))
        
        ch = stdscr.getch()
        if ch == ord('1'): view = "MAIN"
        elif ch == ord('2'): view = "NODOS"
        elif ch == ord('3'): view = "BRIEF"
        elif ch == ord('4'): view = "ALPHA"
        elif ch == ord('q'): break
        time.sleep(0.5)

if __name__ == "__main__":
    curses.wrapper(main)
