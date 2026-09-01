@echo off
echo Setting up Data Centre EPC Platform...
if not exist .env copy .env.example .env
cd backend
if not exist venv python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
cd ..\frontend
if not exist .env.local copy .env.example .env.local
call npm install
cd ..
echo Setup Completed!
