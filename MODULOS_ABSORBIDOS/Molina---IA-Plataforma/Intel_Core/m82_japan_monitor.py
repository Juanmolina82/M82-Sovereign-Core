def evaluate_japan_exposure(industrial_output_change, oil_dependency):
    if industrial_output_change < 0 and oil_dependency >= 0.95:
        return "JAPAN_MACRO_CRITICAL"
    return "STABLE"