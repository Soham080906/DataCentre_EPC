#!/usr/bin/env bash
set -e
if [ ! -f .env ]; then cp .env.example .env; fi
cd backend
if [ ! -d "venv" ]; then python3 -m venv venv; fi
source venv/bin/activate
pip install -r requirements.txt
cd ../frontend
if [ ! -f .env.local ]; then cp .env.example .env.local; fi
npm install
cd ..
echo "Setup Completed!"
