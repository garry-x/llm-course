#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# LLM Learner — 本地开发 & Docker 部署
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMAGE_NAME="${LLM_IMAGE:-llm-learner}"
CONTAINER_NAME="${LLM_CONTAINER:-llm-learner}"
DEFAULT_HOST="${LLM_HOST:-0.0.0.0}"
DEFAULT_PORT="${LLM_PORT:-8080}"

# ---- 颜色 ----
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

usage() {
  cat <<EOF
用法: $0 <命令> [选项]

LLM 深度学习课程 — 本地开发 & Docker 部署

命令:
  serve               启动本地开发服务器 (python/http-server)
  docker-build        构建 Docker 镜像
  docker-up           启动 Docker 容器 (后台运行)
  docker-down         停止 Docker 容器
  docker-logs         查看 Docker 容器日志
  docker-restart      重启 Docker 容器

选项:
  -h, --host HOST     监听地址 (默认: $DEFAULT_HOST, 仅 serve)
  -p, --port PORT     监听端口 (默认: $DEFAULT_PORT)
  --help              显示此帮助信息

环境变量:
  LLM_HOST / LLM_PORT  本地服务器地址/端口
  LLM_IMAGE            Docker 镜像名 (默认: llm-learner)
  LLM_CONTAINER        Docker 容器名 (默认: llm-learner)

示例:
  $0 serve                       # 本地开发服务器 :8080
  $0 serve -p 3000               # 本地开发服务器 :3000
  $0 docker-build                # 构建镜像 (默认端口 8080)
  $0 docker-build -p 3000        # 构建镜像 (默认端口 3000)
  $0 docker-up                   # Docker 启动 (:8080)
  $0 docker-up -p 3000           # Docker 启动 (:3000)
  $0 docker-logs                 # 查看日志
  $0 docker-down                 # 停止容器

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

cmd_docker_build() {
  local port="${DEFAULT_PORT}"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -p|--port) port="$2"; shift 2 ;;
      *) echo -e "${RED}未知参数: $1${NC}"; usage ;;
    esac
  done

  banner
  echo -e "  模式:    ${GREEN}Docker 构建${NC}"
  echo -e "  镜像:    ${IMAGE_NAME}:latest"
  echo -e "  默认端口: ${port}"
  echo ""

  cd "$SCRIPT_DIR"
  docker build --build-arg LISTEN_PORT="${port}" -t "${IMAGE_NAME}:latest" .
  echo ""
  echo -e "${GREEN}✓ 镜像构建完成: ${IMAGE_NAME}:latest${NC}"
  echo -e "  容器端口: ${port}"
  echo -e "  运行: ${YELLOW}$0 docker-up -p ${port}${NC}"
}

cmd_docker_up() {
  local port="${DEFAULT_PORT}"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -p|--port) port="$2"; shift 2 ;;
      *) echo -e "${RED}未知参数: $1${NC}"; usage ;;
    esac
  done

  # 检查镜像是否存在
  if ! docker image inspect "${IMAGE_NAME}:latest" &>/dev/null; then
    echo -e "${YELLOW}镜像不存在，先构建...${NC}"
    cmd_docker_build -p "$port"
  fi

  # 停止旧容器
  docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

  check_port "$port" && kill_port "$port"

  banner
  echo -e "  模式:    ${GREEN}Docker 运行${NC}"
  echo -e "  地址:    ${GREEN}http://0.0.0.0:${port}${NC}"
  echo -e "  容器:    ${CONTAINER_NAME}"
  echo -e "  日志:    ${YELLOW}$0 docker-logs${NC}"
  echo ""

  docker run -d \
    --name "$CONTAINER_NAME" \
    -p "${port}:${port}" \
    --restart unless-stopped \
    "${IMAGE_NAME}:latest"

  echo -e "${GREEN}✓ 容器已启动${NC}"
}

cmd_docker_down() {
  if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    echo -e "${GREEN}✓ 容器已停止并删除${NC}"
  else
    echo -e "${YELLOW}容器 ${CONTAINER_NAME} 未运行${NC}"
  fi
}

cmd_docker_logs() {
  docker logs -f "$CONTAINER_NAME"
}

cmd_docker_restart() {
  cmd_docker_down
  cmd_docker_up
}

# ================================================================
# 主入口
# ================================================================

CMD="${1:-serve}"
shift || true

case "$CMD" in
  serve)           cmd_serve "$@" ;;
  docker-build)    cmd_docker_build "$@" ;;
  docker-up)       cmd_docker_up "$@" ;;
  docker-down)     cmd_docker_down "$@" ;;
  docker-logs)     cmd_docker_logs "$@" ;;
  docker-restart)  cmd_docker_restart "$@" ;;
  -h|--help|help)  usage ;;
  *) echo -e "${RED}未知命令: $CMD${NC}"; usage ;;
esac
