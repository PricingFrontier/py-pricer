FROM python:3.10-slim

WORKDIR /app

# Install UV
RUN pip install --no-cache-dir uv

# Copy project configuration first for better caching
COPY pyproject.toml .

# Use UV to install dependencies from pyproject.toml
RUN uv pip install --no-cache-dir .

# Copy only the necessary files
COPY api/ ./api/
COPY algorithms/ ./algorithms/
COPY streamlit/ ./streamlit/
COPY py_pricer/ ./py_pricer/
COPY logs/ ./logs/

# Make port 8000 available
EXPOSE 8000

# Set environment variables
ENV PORT=8000
ENV HOST=0.0.0.0

# Run the API with Gunicorn for production
CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 api.api:app 