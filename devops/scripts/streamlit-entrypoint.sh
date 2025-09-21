#!/bin/bash
set -e

echo "🔍 Starting Streamlit application..."

# Wait for backend to be available (optional health check)
echo "⏳ Waiting for backend to be ready..."
while ! curl -f http://venture-vision-backend-server:${BACKEND_PORT:-5000}/api/v1/health &>/dev/null; do
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