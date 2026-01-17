#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
source "$PROJECT_ROOT/.venv/bin/activate"

# 关键：确保工作目录为项目根目录
cd "$PROJECT_ROOT" || exit 1

# 设置 PYTHONPATH 确保模块可被找到
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# 设置环境变量
export REDIS_HOST=${REDIS_HOST:-localhost}
export REDIS_PORT=${REDIS_PORT:-16379}
export CELERY_BROKER_DB=${CELERY_BROKER_DB:-1}
export CELERY_RESULT_BACKEND_DB=${CELERY_RESULT_BACKEND_DB:-1}

# 启动 Celery Worker（移除 --workdir 参数）
celery -A config.config worker \
    --loglevel=info \
    --hostname=llmops-worker@%h
