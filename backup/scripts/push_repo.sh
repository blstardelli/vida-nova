#!/bin/bash
# uso: ./push_repo.sh "mensagem"
set -e
cd /home/claude
R=/home/claude/vida-nova
git -C $R fetch -q --depth=1 origin main && git -C $R checkout -q main && git -C $R reset -q --hard origin/main
cp site/index.html $R/index.html
mkdir -p $R/backup/dados $R/backup/scripts
cp out/refeicoes.json out/diario.json out/ff_prato.json out/alimentos_dia.json $R/backup/dados/
cp open_day.json $R/backup/open_day.json
cp REGRAS.md $R/backup/REGRAS.md
cp build_site.py publish_open_day.py push_repo.sh site_template.html make_alim2.py make_saciedade.py make_backup.py $R/backup/scripts/
git -C $R add -A
git -C $R -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -qm "$1

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01AdgWHwxQjF2UHKp3i8pCcM" || echo "nada a commitar"
git -C $R -c push.negotiate=true push origin main 2>&1 | tail -2
