#!/usr/bin/env bash
# =============================================================================
# stop.sh — Stops the Databricks ETL Agent Docker container (and local app)
# =============================================================================
set -euo pipefail

APP_NAME="databricks-etl-agent"
CONTAINER_NAME="${APP_NAME}"
IMAGE_NAME="${APP_NAME}:latest"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log()      { echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] [INFO]${NC}  $*"; }
log_ok()   { echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] [OK]${NC}    $*"; }
log_warn() { echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] [WARN]${NC}  $*"; }

log "Stopping Databricks ETL Agent..."

if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        log "Stopping container '${CONTAINER_NAME}'..."
        docker stop "${CONTAINER_NAME}" >/dev/null
        log_ok "Container stopped."
    else
        log_warn "No running container named '${CONTAINER_NAME}'."
    fi

    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        log "Removing container '${CONTAINER_NAME}'..."
        docker rm "${CONTAINER_NAME}" >/dev/null
        log_ok "Container removed."
    fi

    if [ "${1:-}" = "--remove-image" ]; then
        if docker images -q "${IMAGE_NAME}" | grep -q .; then
            log "Removing image '${IMAGE_NAME}'..."
            docker rmi "${IMAGE_NAME}" >/dev/null
            log_ok "Image removed."
        else
            log_warn "Image '${IMAGE_NAME}' not found."
        fi
    fi
else
    log_warn "Docker not available — skipping container cleanup."
fi

# Also stop any locally running Streamlit instance of this app
if pgrep -f "streamlit run streamlit_app/app.py" >/dev/null 2>&1; then
    log "Stopping local Streamlit process..."
    pkill -f "streamlit run streamlit_app/app.py" || true
    log_ok "Local Streamlit stopped."
fi

log_ok "Done."
