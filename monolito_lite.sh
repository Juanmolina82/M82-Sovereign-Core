#!/bin/bash
echo "=== M82 MONOLITO LITE RUNNING (PID ÚNICO) ==="

while true; do
    sqlite3 ~/M82/m82_database.db << 'SQL_EOF'
    BEGIN TRANSACTION;
    UPDATE m82_daemons_registry SET status = 'LITE' WHERE status != 'OFFLINE';
    COMMIT;
SQL_EOF

    sleep 3
done
