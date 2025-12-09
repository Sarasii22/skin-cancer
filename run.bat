@echo off
cd /d %~dp0
docker compose down --remove-orphans
docker compose up --build
pause