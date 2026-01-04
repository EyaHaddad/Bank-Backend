@echo off
REM Export de la base de données locale vers Docker
echo === Export de la base banking_db ===

docker run --rm -e PGPASSWORD=hmd202303 postgres:18-alpine pg_dump -h host.docker.internal -p 5433 -U postgres -d banking_db --no-owner --no-acl --if-exists --clean > docker\init-db\01-data.sql 2>nul

if %errorlevel% equ 0 (
    echo Export OK: docker\init-db\01-data.sql
) else (
    echo ERREUR: Verifiez que Docker Desktop et PostgreSQL sont actifs
)
pause
