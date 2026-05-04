def validate_ticker_signal(news_alert):
    if "KKR" in news_alert and "government contractor" in news_alert:
        return "ERROR_TAG_DETECTED"
    if "Engine Capital" in news_alert and "KBR" in news_alert:
        return "VALID_ACTIVIST_SIGNAL"
    return "NEUTRAL"