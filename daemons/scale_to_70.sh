#!/bin/bash
BASE=~/M82
for i in {61..70}; do
    case $i in
        61|62|63|64) SRC="ASIA_CHIP_RALLY_KS11_SAMSUNG_HYNIX" ;;
        65|66|67)    SRC="AI_INFRA_PROXY_SMCI_MICRON_NVDA" ;;
        68|69)       SRC="FX_CARRY_YEN_USDJPY_RATES" ;;
        70)          SRC="ENTROPY_FEED_AGI_KRONOS" ;;
    esac
    nohup python3 $BASE/daemons/m82_daemon_core.py --id $i --source $SRC --mode LISTEN --bunker 0.30 --alpha 0.89 >> $BASE/logs/daemon_$i.log 2>&1 &
    echo "Daemon $i [$SRC] deployed PID $!"
done
