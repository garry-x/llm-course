#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# LLM Learner — Local Development Server
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_HOST="${LLM_HOST:-0.0.0.0}"
DEFAULT_PORT="${LLM_PORT:-8080}"

# ---- Colors ----
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

usage() {
  cat <<EOF
Usage: $0 <command> [options]

LLM Deep Learning Course — Local Development Server

Commands:
  serve               Start local development server (python/http-server)

Options:
  -h, --host HOST     Listen address (default: $DEFAULT_HOST)
  -p, --port PORT     Listen port (default: $DEFAULT_PORT)
  --help              Show this help message

Environment Variables:
  LLM_HOST / LLM_PORT  Local server address/port

Examples:
  $0 serve                       # Local development server :8080
  $0 serve -p 3000               # Local development server :3000

EOF
  exit 0
}

# ---- Port Check ----
check_port() {
  local port="$1"
  if command -v ss &>/dev/null; then
    ss -tlnp | grep -q ":$port " 2>/dev/null && return 0
  elif command -v lsof &>/dev/null; then
    lsof -Pi :"$port" -sTCP:LISTEN -t >/dev/null 2>&1 && return 0
  fi
  return 1
}

kill_port() {
  local port="$1"
  echo -e "${YELLOW}⚠ Port $port is already in use${NC}"
  if command -v ss &>/dev/null; then
    local pid=$(ss -tlnp | grep ":$port " | grep -oP 'pid=\K\d+' | head -1)
  elif command -v lsof &>/dev/null; then
    local pid=$(lsof -Pi :"$port" -sTCP:LISTEN -t 2>/dev/null)
  fi
  if [ -n "${pid:-}" ]; then
    read -rp "Terminate PID $pid? [y/N] " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
      kill "$pid" 2>/dev/null && echo -e "${GREEN}✓ Terminated${NC}"
      sleep 0.5
    else
      echo "Cancelled"; exit 1
    fi
  fi
}

banner() {
  echo -e "${CYAN}╔══════════════════════════════════════════╗${NC}"
  echo -e "${CYAN}║   🧠 LLM Deep Learning Course           ║${NC}"
  echo -e "${CYAN}╚══════════════════════════════════════════╝${NC}"
  echo ""
}

display_host() {
  local host="$1"
  if [ "$host" = "0.0.0.0" ] || [ "$host" = "::" ]; then
    echo "127.0.0.1"
  else
    echo "$host"
  fi
}

# ================================================================
# Command Implementations
# ================================================================

cmd_serve() {
  local host="$DEFAULT_HOST" port="$DEFAULT_PORT"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -h|--host) host="$2"; shift 2 ;;
      -p|--port) port="$2"; shift 2 ;;
      --help) usage ;;
      *) echo -e "${RED}Unknown parameter: $1${NC}"; usage ;;
    esac
  done

  check_port "$port" && kill_port "$port"

  banner
  local browser_host
  browser_host="$(display_host "$host")"
  echo -e "  Mode:    ${GREEN}Local Development${NC}"
  echo -e "  Local:   ${GREEN}http://${browser_host}:${port}${NC}"
  if [ "$host" = "0.0.0.0" ] || [ "$host" = "::" ]; then
    echo -e "  Listen:  ${YELLOW}${host}:${port}${NC} (use your machine IP for LAN access)"
  else
    echo -e "  Listen:  ${YELLOW}${host}:${port}${NC}"
  fi
  echo -e "  Directory: ${SCRIPT_DIR}"
  echo -e "  Stop:    ${YELLOW}Ctrl+C${NC}"
  echo ""

  cd "$SCRIPT_DIR"
  if command -v python3 &>/dev/null; then
    python3 -m http.server "$port" --bind "$host"
  elif command -v python &>/dev/null; then
    python -m http.server "$port" --bind "$host"
  elif command -v npx &>/dev/null; then
    npx http-server "$SCRIPT_DIR" -a "$host" -p "$port"
  else
    echo -e "${RED}Error: python3 / python / npx not found${NC}"
    exit 1
  fi
}

# ================================================================
# Main Entry Point
# ================================================================

CMD="${1:-serve}"
shift || true

case "$CMD" in
  serve)           cmd_serve "$@" ;;
  -h|--help|help)  usage ;;
  *) echo -e "${RED}Unknown command: $CMD${NC}"; usage ;;
esac
