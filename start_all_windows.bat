@echo off

:: This script starts all services for the application
:: Just run "./start_all_windows.bat" in your bash script

:: Start UI_NeuralCheck
start "UI_NeuralCheck" cmd /k "cd UI_NeuralCheck && npm run dev"

:: Start authentifizierungs-service
start "authentifizierungs-service" cmd /k "cd authentifizierungs-service && python auth.py"

:: Start trainingsorchestrator-service
start "trainingsorchestrator-service" cmd /k "cd trainingsorchestrator-service && python orchestrator.py"

:: Start data-service
start "data-service" cmd /k "cd data-service && python app_data.py"

:: Start Trainingsservice
start "Trainingsservice" cmd /k "cd Trainingsservice && python app.py"
