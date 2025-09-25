#!/usr/bin/env bash
set -euo pipefail

# Create folders if they don't exist
mkdir -p backend frontend shared uploads

# Move known files into the new structure if present
[ -f main.py ]   && mv -vn main.py backend/main.py
[ -f agent.py ]  && mv -vn agent.py shared/agent.py
[ -f vector.py ] && mv -vn vector.py shared/vector.py
[ -f app.py ]    && mv -vn app.py frontend/app.py

echo '✅ Restructure complete.'
echo '- backend/: main.py, agent.py, vector.py'
echo '- frontend/: app.py'
echo '- shared/: (place shared utils here as needed)'
echo '- uploads/: (put .pdf/.txt/.pptx here)'
echo ''
echo 'Review imports if you moved modules across packages.'
