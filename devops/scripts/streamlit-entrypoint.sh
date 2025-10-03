#!/bin/bash
set -e

echo "🔍 Starting Streamlit application..."

# Wait for backend to be available (optional health check)
echo "⏳ Waiting for backend to be ready..."
echo "API_BASE_URL: ${API_BASE_URL:-http://localhost:8000}"
while ! curl -f ${API_BASE_URL:-http://localhost:8000}/api/v1/health &>/dev/null; do
    echo "Backend not ready yet, waiting..."
    sleep 2
done

echo "✅ Backend is ready!"
echo "🌐 Starting Streamlit application..."

# Start Streamlit with proper configuration
exec uv run streamlit run /src/streamlit/streamlit_app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.fileWatcherType=none \
    --browser.gatherUsageStats=false 