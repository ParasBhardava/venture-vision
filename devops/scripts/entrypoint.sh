#!/bin/bash
set -e

# Show debug information
echo "🔍 Environment validation..."
# Check for essential database environment variables
# if [ -z "$POSTGRES_DATABASE_HOST" ] || [ -z "$POSTGRES_DATABASE_USERNAME" ] || [ -z "$POSTGRES_DATABASE_PASSWORD" ] || [ -z "$POSTGRES_DATABASE_NAME" ]; then
#   echo "❌ ERROR: Required database environment variables are not set"
#   echo "Required variables: POSTGRES_DATABASE_HOST, POSTGRES_DATABASE_USERNAME, POSTGRES_DATABASE_PASSWORD, POSTGRES_DATABASE_NAME"
#   exit 1
# fi

# Apply migrations with error logging but continue regardless
# echo "🚀 Running database migrations..."
# SQLALCHEMY_SILENCE_UBER_WARNING=1 uv run alembic upgrade head || {
#   echo "⚠️ Migration failed with error code $? - continuing anyway"
# }

# Mark migrations as completed
# echo "✅ Marking migrations as completed"
# uv run alembic stamp head || {
#   echo "⚠️ Failed to stamp migrations - continuing anyway"
# }

echo "🌐 Starting application..."

# Start the application
exec uv run python -m main
