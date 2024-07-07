#!/bin/bash

# This script starts all services for the application
# Use the following commands in your shell script
# Change the variable APP_DIR to the path where you NeuralCheck App lies
# Change the variable CONDA_ENV_NAME to the name of your python environment
# Make the script executable: "chmod +x start_all_linux_macOS.sh"
# Run the script: "./start_all.sh"

APP_DIR="~/Programmieren/Uni/Master/NeuralCheck"
CONDA_ENV_NAME="tensi"

# Start the UI_NeuralCheck service
osascript -e "tell application \"Terminal\" to do script \"cd $APP_DIR/UI_NeuralCheck && npm run dev\""

# Start the authentifizierungs-service
osascript -e "tell application \"Terminal\" to do script \"source activate $CONDA_ENV_NAME && cd $APP_DIR/authentifizierungs-service && python app/auth.py\""

# Start the trainingsorchestrator-service
osascript -e "tell application \"Terminal\" to do script \"source activate $CONDA_ENV_NAME && cd $APP_DIR/trainingsorchestrator-service && python app/orchestrator.py\""

# Start the data-service
osascript -e "tell application \"Terminal\" to do script \"source activate $CONDA_ENV_NAME && cd $APP_DIR/data-service && python app/app_data.py\""

# Start the Trainingsservice
osascript -e "tell application \"Terminal\" to do script \"source activate $CONDA_ENV_NAME && cd $APP_DIR/Trainingsservice && python app.py\""
