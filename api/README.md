# Insurance Pricing API

This API provides endpoints for processing insurance quotes and calculating premiums, using FastAPI and following a RESTful design.

## Table of Contents
- [Quick Start](#quick-start)
  - [Local Development](#local-development)
  - [Deploy to Azure](#deploy-to-azure)
- [API Overview](#api-overview)
  - [Endpoints](#endpoints)
  - [Request & Response Format](#request--response-format)
  - [API Documentation](#api-documentation)
  - [Error Handling](#error-handling)
- [Azure Deployment Details](#azure-deployment-details)
  - [Prerequisites](#prerequisites)
  - [Scaling Information](#scaling-information)
  - [Monitoring](#monitoring)
  - [Troubleshooting](#troubleshooting)

## Quick Start

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/your-username/py-pricer.git
cd py-pricer

# 2. Run the initialization command
pypricer-init

# OR if the command isn't available yet:
./prepare_local_env.sh
```

The initialization script will:
- Install UV package manager if needed
- Create a virtual environment
- Install all dependencies from pyproject.toml
- Set up pre-commit hooks (if configured)

To run the API locally:
```bash
pypricer-api
```

To test the API:
```bash
python -m pytest api/test_api.py -v
```

### Deploy to Azure

```bash
# 1. Clone the repository
git clone https://github.com/your-username/py-pricer.git
cd py-pricer

# 2. Initialize the environment (if not already done)
pypricer-init

# 3. Run the deployment command
pypricer-deploy

# OR if the command isn't available:
chmod +x api/deploy.sh
./api/deploy.sh
```

The script will guide you through the deployment process with clear instructions.

## API Overview

The API processes insurance quote data through the same transformation pipeline and rating engine used by the Streamlit application.

### Endpoints

#### Health Check
```
GET /health
```
Returns the health status of the API.

#### Process Quote
```
POST /quote
```
Processes a quote through the transformation pipeline and rating engine, returning the calculated premium details.

### Request & Response Format

Request:
```json
{
  "data": {
    "IDpol": 1,
    "VehPower": 5,
    "VehAge": 2,
    "DrivAge": 30,
    "BonusMalus": 50,
    "VehBrand": "B1",
    "VehGas": "Regular",
    "Area": "A",
    "Density": 800,
    "Region": "R1"
  }
}
```

Response:
```json
{
  "quote_id": "1",
  "premium_details": {
    "base_premium": 200,
    "premium_after_veh_age": 260,
    "final_premium": 312
  }
}
```

### API Documentation

When the API is running, you can access the auto-generated documentation at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Error Handling

The API returns appropriate HTTP status codes and error messages:
- 200: Successful request
- 400: Bad request (e.g., invalid data format)
- 500: Internal server error

Error responses include an error message and optional details.

## Azure Deployment Details

### Prerequisites

Before deployment, ensure you have:

1. **Azure Account**: Create one at [https://azure.microsoft.com](https://azure.microsoft.com)
2. **Azure CLI**: Install from [https://docs.microsoft.com/en-us/cli/azure/install-azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
3. **Docker**: Install from [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
4. **UV**: For package management

Installation commands:

<details>
<summary>Ubuntu/Debian</summary>

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install Docker
sudo apt-get update
sudo apt-get install docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Install UV
pip install uv
```
</details>

<details>
<summary>macOS</summary>

```bash
# Install Azure CLI
brew update && brew install azure-cli

# Install Docker Desktop from https://docs.docker.com/desktop/mac/install/

# Install UV
pip install uv
```
</details>

<details>
<summary>Windows</summary>

```bash
# Install Azure CLI with PowerShell
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; rm .\AzureCLI.msi

# Install Docker Desktop from https://docs.docker.com/desktop/windows/install/

# Install UV
pip install uv
```
</details>

The deployment script will:
1. Create a resource group in Azure
2. Create an Azure Container Registry
3. Build your API as a Docker container
4. Push the container to the registry
5. Deploy the container to Azure Container Apps
6. Configure scaling to handle high traffic
7. Display the URL where your API is running

You can customize deployment by editing variables in `api/deploy.sh`:
```bash
# Configuration values
RESOURCE_GROUP="pyPricerGroup"
LOCATION="eastus"
CONTAINER_APP_NAME="py-pricer-api"
CONTAINER_APP_ENV="py-pricer-env"
IMAGE_NAME="py-pricer-api"
```

### Scaling Information

The deployment is configured to handle approximately 500,000 requests per day:
- **Minimum Replicas**: 1 (always at least one instance running)
- **Maximum Replicas**: 10 (can scale up to 10 instances during high traffic)
- **Scaling Rule**: Based on HTTP concurrency (100 concurrent requests per instance)
- **Resources**: Each instance has 0.5 CPU cores and 1GB memory

### Monitoring

To monitor your API:
1. Go to the [Azure Portal](https://portal.azure.com)
2. Navigate to your resource group (default: "pyPricerGroup")
3. Click on your Container App (default: "py-pricer-api")
4. View the "Monitoring" tab for metrics

### Troubleshooting

<details>
<summary>Check Logs</summary>

```bash
# View logs from your Container App
az containerapp logs show --name py-pricer-api --resource-group pyPricerGroup
```
</details>

<details>
<summary>Test Docker Locally</summary>

```bash
# Build Docker image locally
docker build -t py-pricer-api -f api/Dockerfile .

# Run the container locally
docker run -p 8000:8000 py-pricer-api

# In another terminal, test the local API
curl http://localhost:8000/health
```
</details>

<details>
<summary>Common Issues</summary>

- **Resource Quota Issues**: You might need to request quota increases for certain regions
- **Authentication Errors**: Run `az login` again
- **Network Issues**: Ensure your firewall allows outbound connections to Azure
- **Dependency Management Issues**: If there are issues with dependencies in the container, make sure your pyproject.toml file is correctly set up
- **UV Issues**: Consult the [UV Documentation](https://github.com/astral-sh/uv)
</details>

<details>
<summary>Clean Up Resources</summary>

```bash
# Delete the resource group and all resources
az group delete --name pyPricerGroup --yes
```
</details>

### Additional Resources

- [Azure Container Apps Documentation](https://docs.microsoft.com/en-us/azure/container-apps/)
- [Azure CLI Reference](https://docs.microsoft.com/en-us/cli/azure/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/)
- [UV Documentation](https://github.com/astral-sh/uv)
- [Python Packaging with pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) 