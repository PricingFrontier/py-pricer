#!/bin/bash

# Exit on any error
set -e

# Display banner
echo "=========================================================="
echo "                PY-PRICER API DEPLOYMENT                  "
echo "=========================================================="
echo "This script will deploy the Pricing API to Azure Container Apps"

# Configuration - change these values
RESOURCE_GROUP="pyPricerGroup"
LOCATION="eastus"
CONTAINER_APP_NAME="py-pricer-api"
CONTAINER_APP_ENV="py-pricer-env"
IMAGE_NAME="py-pricer-api"

# Display configuration
echo ""
echo "📋 DEPLOYMENT CONFIGURATION:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  Container App: $CONTAINER_APP_NAME"
echo "  Environment: $CONTAINER_APP_ENV"
echo ""

# Confirm with user
read -p "Continue with deployment? (y/n): " confirm
if [[ $confirm != "y" && $confirm != "Y" ]]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""
echo "🔄 Checking Azure CLI login status..."
# Check if user is logged in
if ! az account show > /dev/null 2>&1; then
    echo "⚠️ You're not logged in to Azure CLI."
    echo "🔑 Please login now:"
    az login
    if [ $? -ne 0 ]; then
        echo "❌ Login failed. Please try again."
        exit 1
    fi
    echo "✅ Login successful!"
else
    echo "✅ Already logged in!"
fi

# Create resource group if it doesn't exist
echo ""
echo "🔄 Creating resource group $RESOURCE_GROUP if it doesn't exist..."
az group create --name $RESOURCE_GROUP --location $LOCATION --only-show-errors || true
echo "✅ Resource group ready!"

# Create container registry if it doesn't exist
echo ""
echo "🔄 Creating container registry..."
REGISTRY_NAME="${RESOURCE_GROUP}registry"
REGISTRY_NAME=${REGISTRY_NAME//[^a-zA-Z0-9]/}
REGISTRY_NAME=$(echo "$REGISTRY_NAME" | tr '[:upper:]' '[:lower:]')

az acr create --resource-group $RESOURCE_GROUP --name $REGISTRY_NAME --sku Basic --admin-enabled true --only-show-errors || true
echo "✅ Container registry ready!"

# Get registry credentials
echo ""
echo "🔄 Getting registry credentials..."
REGISTRY_URL=$(az acr show --name $REGISTRY_NAME --query loginServer -o tsv)
REGISTRY_USERNAME=$(az acr credential show --name $REGISTRY_NAME --query username -o tsv)
REGISTRY_PASSWORD=$(az acr credential show --name $REGISTRY_NAME --query passwords[0].value -o tsv)
echo "✅ Credentials obtained!"

# Build and push Docker image
echo ""
echo "🔄 Building and pushing Docker image..."
echo "  This may take a few minutes..."
az acr build --registry $REGISTRY_NAME --image $IMAGE_NAME:latest --file api/Dockerfile .
echo "✅ Container image built and pushed!"

# Create container app environment if it doesn't exist
echo ""
echo "🔄 Creating container app environment..."
az containerapp env create \
  --name $CONTAINER_APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --only-show-errors || true
echo "✅ Container app environment ready!"

# Deploy container app
echo ""
echo "🔄 Deploying container app..."
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image "$REGISTRY_URL/$IMAGE_NAME:latest" \
  --registry-server $REGISTRY_URL \
  --registry-username $REGISTRY_USERNAME \
  --registry-password $REGISTRY_PASSWORD \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 10 \
  --scale-rule-name http-rule \
  --scale-rule-http-concurrency 100 \
  --cpu 0.5 \
  --memory 1.0Gi \
  --only-show-errors
echo "✅ Container app deployed!"

# Get the application URL
APP_URL=$(az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)

echo ""
echo "🎉 DEPLOYMENT COMPLETE! 🎉"
echo "==========================================="
echo "🌐 Your API is available at: https://$APP_URL"
echo "📚 Documentation: https://$APP_URL/docs"
echo ""
echo "🔍 Test with: curl https://$APP_URL/health"
echo ""
echo "📊 View in Azure Portal: https://portal.azure.com/#@/resource/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.App/containerApps/$CONTAINER_APP_NAME"
echo "===========================================" 