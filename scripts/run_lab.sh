#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip >/dev/null
pip install -r src/auth-service/requirements.txt \
            -r src/accounts-service/requirements.txt \
            -r src/audit-service/requirements.txt >/dev/null

echo "[run_lab] Starting services..."

# Start each service in its own background process and port.
uvicorn src.auth-service.app:app --port 8001 --reload &
AUTH_PID=$!
uvicorn src.accounts-service.app:app --port 8002 --reload &
ACCOUNTS_PID=$!
uvicorn src.audit-service.app:app --port 8003 --reload &
AUDIT_PID=$!

trap 'echo "[run_lab] Stopping services"; kill $AUTH_PID $ACCOUNTS_PID $AUDIT_PID 2>/dev/null || true' INT TERM

echo "[run_lab] auth-service:     http://localhost:8001"
echo "[run_lab] accounts-service: http://localhost:8002"
echo "[run_lab] audit-service:    http://localhost:8003"
echo "[run_lab] Press Ctrl+C to stop."

wait
