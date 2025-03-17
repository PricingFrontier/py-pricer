# Python Insurance Pricing Library

## Available CLI Commands

This package provides several useful command-line tools to make development and deployment easier:

| Command | Description |
|---------|-------------|
| `pypricer-init` | Initialize the development environment (creates venv, installs dependencies) |
| `pypricer-api` | Run the API server locally |
| `pypricer-ui` | Run the Streamlit UI locally |
| `pypricer-deploy` | Deploy the API to Azure Container Apps |

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/py-pricer.git
cd py-pricer

# Initialize the environment
./prepare_local_env.sh

# After initialization, you can use the commands:
pypricer-ui     # Run the UI
pypricer-api    # Run the API
pypricer-deploy # Deploy to Azure
```

For detailed documentation, see the [API README](api/README.md) or [Streamlit UI documentation](streamlit/README.md).
