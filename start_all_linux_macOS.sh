#!/bin/bash

# This script starts all services for the application
# Use the following commands in your shell script
# Make the script executable: "chmod +x start_all.sh"
# Run the script: "./start_all.sh"

# Start the UI_NeuralCheck service
gnome-terminal -- bash -c "cd UI_NeuralCheck && npm run dev; exec bash"

# Start the authentifizierungs-service
gnome-terminal -- bash -c "cd authentifizierungs-service && python app/auth.py; exec bash"

# Start the trainingsorchestrator-service
gnome-terminal -- bash -c "cd trainingsorchestrator-service && python app/orchestrator.py; exec bash"

# Start the data-service
gnome-terminal -- bash -c "cd data-service && python app/app_data.py; exec bash"

# Start the Trainingsservice
gnome-terminal -- bash -c "cd Trainingsservice && python app.py; exec bash"
