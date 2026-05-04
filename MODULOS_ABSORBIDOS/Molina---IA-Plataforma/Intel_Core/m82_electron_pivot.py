def analyze_transition_alpha(ev_growth_rate, oil_price):
    if oil_price > 115 and ev_growth_rate > 1.0:
        return "ACCELERATED_ELECTRIFICATION_HEDGE"
    return "MONITOR_RAW_MATERIALS"