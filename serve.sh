#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# LLM Learner — 本地开发服务器
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_HOST="${LLM_HOST:-0.0.0.0}"
DEFAULT_PORT="${LLM_PORT:-8080}"

# ---- 颜色 ----
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

usage() {
  cat <<EOF
用法: $0 <命令> [选项]

LLM 深度学习课程 — 本地开发服务器

命令:
  serve               启动本地开发服务器 (python/http-server)

选项:
  -h, --host HOST     监听地址 (默认: $DEFAULT_HOST)
  -p, --port PORT     监听端口 (默认: $DEFAULT_PORT)
  --help              显示此帮助信息

环境变量:
  LLM_HOST / LLM_PORT  本地服务器地址/端口

示例:
  $0 serve                       # 本地开发服务器 :8080
  $0 serve -p 3000               # 本地开发服务器 :3000

EOF
  exit 0
}

# ---- 端口检查 ----
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
  echo -e "${YELLOW}⚠ 端口 $port 已被占用${NC}"
  if command -v ss &>/dev/null; then
    local pid=$(ss -tlnp | grep ":$port " | grep -oP 'pid=\K\d+' | head -1)
  elif command -v lsof &>/dev/null; then
    local pid=$(lsof -Pi :"$port" -sTCP:LISTEN -t 2>/dev/null)
  fi
  if [ -n "${pid:-}" ]; then
    read -rp "是否终止 PID $pid? [y/N] " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
      kill "$pid" 2>/dev/null && echo -e "${GREEN}✓ 已终止${NC}"
      sleep 0.5
    else
      echo "已取消"; exit 1
    fi
  fi
}

banner() {
  echo -e "${CYAN}╔══════════════════════════════════════════╗${NC}"
  echo -e "${CYAN}║   🧠 LLM 深度学习课程                    ║${NC}"
  echo -e "${CYAN}╚══════════════════════════════════════════╝${NC}"
  echo ""
}

# ================================================================
# 命令实现
# ================================================================

cmd_serve() {
  local host="$DEFAULT_HOST" port="$DEFAULT_PORT"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -h|--host) host="$2"; shift 2 ;;
      -p|--port) port="$2"; shift 2 ;;
      --help) usage ;;
      *) echo -e "${RED}未知参数: $1${NC}"; usage ;;
    esac
  done

  check_port "$port" && kill_port "$port"

  banner
  echo -e "  模式:    ${GREEN}本地开发${NC}"
  echo -e "  地址:    ${GREEN}http://${host}:${port}${NC}"
  echo -e "  目录:    ${SCRIPT_DIR}"
  echo -e "  停止:    ${YELLOW}Ctrl+C${NC}"
  echo ""

  cd "$SCRIPT_DIR"
  if command -v python3 &>/dev/null; then
    python3 -m http.server "$port" --bind "$host"
  elif command -v python &>/dev/null; then
    python -m http.server "$port" --bind "$host"
  elif command -v npx &>/dev/null; then
    npx http-server "$SCRIPT_DIR" -a "$host" -p "$port"
  else
    echo -e "${RED}错误: 未找到 python3 / python / npx${NC}"
    exit 1
  fi
}

# ================================================================
# 主入口
# ================================================================

CMD="${1:-serve}"
shift || true

case "$CMD" in
  serve)           cmd_serve "$@" ;;
  -h|--help|help)  usage ;;
  *) echo -e "${RED}未知命令: $CMD${NC}"; usage ;;
esac
