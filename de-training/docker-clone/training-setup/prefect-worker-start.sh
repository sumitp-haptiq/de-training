#!/bin/bash
set -e

echo "Waiting for Prefect API to be ready..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if python -c "import urllib.request; urllib.request.urlopen('http://prefect:4200/api/health', timeout=2)" 2>/dev/null; then
        echo "Prefect API is ready!"
        break
    else
        attempt=$((attempt + 1))
        if [ $attempt -lt $max_attempts ]; then
            echo "Prefect API not ready (attempt $attempt/$max_attempts), waiting..."
            sleep 2
        else
            echo "Prefect API did not become ready in time"
            exit 1
        fi
    fi
done

echo "Creating work pool 'local-pool' if it does not exist..."
if ! prefect work-pool inspect local-pool >/dev/null 2>&1; then
    echo "Creating work pool 'local-pool'..."
    prefect work-pool create local-pool --type process || true
else
    echo "Work pool 'local-pool' already exists"
fi

echo "Starting Prefect worker..."
exec prefect worker start --pool local-pool --type process

