#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# LLM Learner — 本地开发服务器启动脚本
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_HOST="${LLM_HOST:-0.0.0.0}"
DEFAULT_PORT="${LLM_PORT:-8080}"

# ---- 颜色 ----
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

usage() {
  cat <<EOF
用法: $0 [选项]

LLM 深度学习课程 — 本地开发服务器

选项:
  -h, --host HOST     监听地址 (默认: $DEFAULT_HOST)
  -p, --port PORT     监听端口 (默认: $DEFAULT_PORT)
  --help              显示此帮助信息

环境变量:
  LLM_HOST            默认监听地址
  LLM_PORT            默认监听端口

示例:
  $0                           # 默认 0.0.0.0:8080
  $0 -p 3000                   # 指定端口 3000
  $0 -h 127.0.0.1 -p 9999      # 仅本地访问

EOF
  exit 0
}

# ---- 参数解析 ----
HOST="$DEFAULT_HOST"
PORT="$DEFAULT_PORT"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--host) HOST="$2"; shift 2 ;;
    -p|--port) PORT="$2"; shift 2 ;;
    --help)    usage ;;
    *) echo -e "${RED}未知参数: $1${NC}"; usage ;;
  esac
done

# ---- 端口占用检查 ----
if lsof -Pi :"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
  PID=$(lsof -Pi :"$PORT" -sTCP:LISTEN -t)
  echo -e "${YELLOW}⚠ 端口 $PORT 已被占用 (PID: $PID)${NC}"
  read -rp "是否终止该进程? [y/N] " answer
  if [[ "$answer" =~ ^[Yy]$ ]]; then
    kill "$PID" 2>/dev/null && echo -e "${GREEN}✓ 已终止 PID $PID${NC}"
    sleep 0.5
  else
    echo "已取消"
    exit 1
  fi
fi

# ---- 启动服务器 ----
echo -e "${CYAN}╔══════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   🧠 LLM 深度学习课程 — 本地服务器      ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "  监听地址: ${GREEN}http://${HOST}:${PORT}${NC}"
echo -e "  课程目录: ${SCRIPT_DIR}"
echo -e "  按 ${YELLOW}Ctrl+C${NC} 停止服务器"
echo ""

# 尝试用多种方式启动，优先 python3
if command -v python3 &>/dev/null; then
  cd "$SCRIPT_DIR"
  python3 -m http.server "$PORT" --bind "$HOST"
elif command -v python &>/dev/null; then
  cd "$SCRIPT_DIR"
  python -m http.server "$PORT" --bind "$HOST"
elif command -v npx &>/dev/null && npx --yes http-server --version >/dev/null 2>&1; then
  npx http-server "$SCRIPT_DIR" -a "$HOST" -p "$PORT"
else
  echo -e "${RED}错误: 未找到 python3 / python / npx，无法启动 HTTP 服务器${NC}"
  exit 1
fi
