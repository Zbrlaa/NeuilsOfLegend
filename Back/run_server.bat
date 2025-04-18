@echo off
echo Lancement du serveur FastAPI...
python -m uvicorn main:app --reload
pause