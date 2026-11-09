#!/data/data/com.termux/files/usr/bin/bash
CSV=~/M82/lseg_export.csv
NTFY=~/M82/scripts/ntfy.sh
[ -f "$CSV" ] || exit 0

get() { grep -i "^$1," "$CSV" 2>/dev/null | head -1 | cut -d, -f2; }

BRENT=$(get LCOc1 || echo "108.00")
WTI=$(get CLc1 || echo "101.13")
MEREY=$(get MEREY16 || echo "93.15")
XAU=$(get "XAU=" || echo "3902.03")
XAG=$(get "XAG=" || echo "50.08")
CRACK=$(get "GL92-SIN-CRK" || echo "9.17")
STOXX=$(get ".STOXX" || echo "-0.10")
ES=$(get ".ESc1" || echo "7646.00")
EUR=$(get "EUR=" || echo "1.083")
NVDA=$(get "NVDA.O" || echo "141.20")
JPM=$(get "JPM" || echo "222.40")
VENZ=$(get "VENZ27=" || echo "50.61")
EWZ=$(get "EWZ" || echo "-27.37")

LOCAL=$(date +"%H:%M %Z")

# 🟢 CANALES BULLISH
$NTFY "🟢 M82 BULLISH [PRECIOUS & MEREY] XAU \$$XAU (+0.7%) | XAG \$$XAG (+2.0%) | MEREY 16 \$$MEREY ITM (Spread \$$14.85) | $LOCAL | Exp:0.22x VaR:1.68%"
$NTFY "🟢 M82 BULLISH [ENERGY & PE] YPF Vaca Muerta +50-75% YoY 2027 | Blackstone Energy V \$8.7B Hard Cap | Anthropic \$16.96B Run-Rate | $LOCAL"

# 🔴 CANALES BEARISH
$NTFY "🔴 M82 BEARISH [REFINING & COMMODITIES] Gasoline Crack \$$CRACK <\$10 (-82% desde récord) | Brent \$$BRENT (-4.5%) WTI \$$WTI | Naphtha \$1,079.50 | $LOCAL"
$NTFY "🔴 M82 BEARISH [TECH & LATAM] STOXX $STOXX% | ES \$$ES | EWZ $EWZ% Lula Shock | AI Capex Caution \$800B->\$1.2T | $LOCAL | Exp:0.22x"

# ⚪ CANALES NEUTRAL / CUSTODIA PASIVA
$NTFY "⚪ M82 BUNKER [FINANCIALS & CREDIT] JPM \$$JPM | BAC \$41.80 | XLF Alpha 8.9 | Warsh 102bps | $LOCAL"
$NTFY "⚪ M82 BUNKER [BONOS VENZ/PDVSA] VENZ 2027 \$$VENZ | PDVSA 2026 \$31.40 | Hold Pasivo 0.30x LOCK | $LOCAL"

echo "$(date -u) CSV->NTFY BULL/BEAR DISPATCH OK" >> ~/M82/logs/csv_ntfy.log
