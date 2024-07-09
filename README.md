# NeuralCheck

**NeuralCheck** simplifies the use of neural networks, allowing non-specialized users to configure and compare the performance of three neural network architectures, making AI solutions more accessible.
This documentation will guide you through setting up the development environment and provide an overview of the available API endpoints and their functionalities.

## Table of Contents
- [Development Environment Setup](#development-environment-setup)
  - [Conda Setup](#conda-setup)
- [API Endpoint Documentation](#api-endpoint-documentation)
  - [Training Service](#training-service)
  - [Trainingsorchestrator Service](#trainingsorchestrator-service)
  - [Authentication Service](#authentication-service)
  - [Data Service](#data-service)
- [Frontend](#frontend)

## Development Environment Setup
### Conda Setup
To setup the development environment, first create a new conda environment and install the requirements. 

```
#Create a new conda environment for the project
conda create -n neural-check python=3.11.5 -y
conda activate neural-check

# Install all packages
pip install -r requirements.txt
```

There are known issues with setting up TensorFlow on a MacBook with an M2 chip, here is a solution:
https://developer.apple.com/metal/tensorflow-plugin/

## API Endpoint Documentation
### Training Service
The Training Service will run under port 8002. The service provides the following interfaces:

| Endpoint          | Description                 |
|-------------------|-----------------------------|
| `GET /dataset/<dataset_name>` | Used to load a dataset.
| `GET /prepare_data` | Used to prepare the data.
| `GET /train`	| Used to train and evaluate the dataset.

### Trainingsorchestrator Service
The Trainingsorchestrator Service will run under port 8001. The service provides the following interfaces:

| Endpoint          | Description                 |
|-------------------|-----------------------------|
| `GET /orch` | Used to process configuration data and returns results.
| `GET /configs/<username>` | Used to return the configurations previously used by a user |

### Authentication Service
The Authentication Service will run under port 8003. The service provides the following interfaces:

| Endpoint          | Description                 |
|-------------------|-----------------------------|
| `POST /register`   | Used to register a user.    |
| `POST /login`      | Used to login the user.     |
| `GET /user`       | Used to get the user data. |
| `POST /validate-auth` | Used to validate the user.|

### Data Service
The Data Service will run under port 8004. The service provides the following interfaces:

| Endpoint          | Description                 |
|-------------------|-----------------------------|
| `GET /default_dataset`| Used to upload the default dataset for a newly registered user |
| `POST /upload_dataset` | Used to upload a new dataset.
| `GET /datasets/<username>` | Used to retrieve all datasets associated with a specific user.
| `GET /dataset/<username/<dataset_name>`	| Used to retrieve a dataset by its specific dataset name for the given user.

## Frontend

Go to the `UI_NeuralCheck` directory and run:
```
npm install
npm run dev
```
Open the browser at http://localhost:5173/.

## Start Application

The scripts `start_all_windows.bat` or `start_all_linux_macOS.sh` start all services required for the application.
Just run `./start_all_windows.bat` in your bash script for Windows. 
For MacOS and Linux, make the script executable `chmod +x start_all.sh` in your shell script and run the script with `./start_all.sh`.

## Run Tests

To run tests for each service, open a terminal and navigate to the designated service directory. Then, execute the command `python -m unittest test`.
