#!/usr/bin/env bash

# 1. Asegurar índice de unicidad y depurar duplicados existentes
sqlite3 ~/M82/m82_database.db << 'SQL_EOF'
DELETE FROM m82_multi_stream 
WHERE id NOT IN (
    SELECT MIN(id) 
    FROM m82_multi_stream 
    GROUP BY headline
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_headline_unique ON m82_multi_stream(headline);
SQL_EOF

# 2. Patching m82_reuters_breakingviews.py para usar INSERT OR IGNORE
sed -i 's/INSERT INTO m82_multi_stream/INSERT OR IGNORE INTO m82_multi_stream/g' ~/M82/m82_reuters_breakingviews.py

# 3. Aplicar a todos los demás daemons por seguridad
sed -i 's/INSERT INTO m82_multi_stream/INSERT OR IGNORE INTO m82_multi_stream/g' ~/M82/m82_*.py

echo "✅ Parche de desduplicación aplicado correctamente en todos los componentes M82."
