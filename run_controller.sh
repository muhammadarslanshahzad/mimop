#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "🤖 Starting MiMoMop external controller..."

source .venv/bin/activate

# Optional: wait for Webots to be ready
sleep 1

python controllers/mimomop_controller/main.py
