#!/usr/bin/env bash
# =============================================================================
# setup.sh — Databricks ETL Agent setup & launch script
#
# 1. Checks prerequisites (python3, pip, docker)
# 2. If Docker is available  -> builds the image and runs the container
# 3. If Docker is unavailable -> creates a venv, installs requirements.txt,
#    and runs the Streamlit UI locally
# =============================================================================
set -euo pipefail

cd "$(dirname "$0")"

# ----------------------------- configuration --------------------------------
APP_NAME="databricks-etl-agent"
IMAGE_NAME="${APP_NAME}:latest"
CONTAINER_NAME="${APP_NAME}"
PORT="${PORT:-8501}"
VENV_DIR=".venv"
LOG_DIR="logs"
LOG_FILE="${LOG_DIR}/setup_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "${LOG_DIR}"

# ------------------------------- logging -------------------------------------
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

log()      { echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] [INFO]${NC}  $*" | tee -a "${LOG_FILE}"; }
log_ok()   { echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] [OK]${NC}    $*" | tee -a "${LOG_FILE}"; }
log_warn() { echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] [WARN]${NC}  $*" | tee -a "${LOG_FILE}"; }
log_err()  { echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR]${NC} $*" | tee -a "${LOG_FILE}"; }

trap 'log_err "Setup failed on line $LINENO. See ${LOG_FILE} for details."' ERR

log "=========================================="
log " Databricks ETL Agent — Setup"
log " Log file: ${LOG_FILE}"
log "=========================================="

# --------------------------- prerequisite checks -----------------------------
log "Checking prerequisites..."

if command -v python3 >/dev/null 2>&1; then
    log_ok "python3 found: $(python3 --version 2>&1)"
else
    log_err "python3 is not installed. Install Python 3.9+ and retry."
    exit 1
fi

DOCKER_AVAILABLE=false
if command -v docker >/dev/null 2>&1; then
    if docker info >/dev/null 2>&1; then
        DOCKER_AVAILABLE=true
        log_ok "Docker found and daemon is running: $(docker --version)"
    else
        log_warn "Docker CLI found but the daemon is not running. Falling back to local mode."
    fi
else
    log_warn "Docker not installed. Falling back to local (venv) mode."
fi

# ------------------------------ docker mode ----------------------------------
if [ "${DOCKER_AVAILABLE}" = true ]; then
    log "Mode: DOCKER"

    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        log_warn "Existing container '${CONTAINER_NAME}' found. Removing it..."
        docker rm -f "${CONTAINER_NAME}" >>"${LOG_FILE}" 2>&1
        log_ok "Old container removed."
    fi

    log "Building Docker image '${IMAGE_NAME}' (this may take a minute)..."
    docker build -t "${IMAGE_NAME}" . 2>&1 | tee -a "${LOG_FILE}"
    log_ok "Image built."

    log "Starting container '${CONTAINER_NAME}' on port ${PORT}..."
    docker run -d --name "${CONTAINER_NAME}" -p "${PORT}:8501" "${IMAGE_NAME}" >>"${LOG_FILE}" 2>&1
    log_ok "Container started."

    log_ok "Streamlit UI is running in Docker: http://localhost:${PORT}"
    log "Follow app logs with:  docker logs -f ${CONTAINER_NAME}"
    log "Stop everything with:  ./stop.sh"
    exit 0
fi

# ------------------------------- local mode ----------------------------------
log "Mode: LOCAL (python venv)"

if [ ! -d "${VENV_DIR}" ]; then
    log "Creating virtual environment at ${VENV_DIR}..."
    python3 -m venv "${VENV_DIR}"
    log_ok "Virtual environment created."
else
    log_ok "Reusing existing virtual environment at ${VENV_DIR}."
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

log "Upgrading pip..."
pip install --upgrade pip >>"${LOG_FILE}" 2>&1
log_ok "pip upgraded: $(pip --version)"

log "Installing dependencies from requirements.txt..."
pip install -r requirements.txt 2>&1 | tee -a "${LOG_FILE}"
log_ok "Dependencies installed."

log_ok "Starting Streamlit UI: http://localhost:${PORT}"
log "Press Ctrl+C to stop."
exec streamlit run streamlit_app/app.py --server.port="${PORT}" --logger.level=info 2>&1 | tee -a "${LOG_FILE}"
