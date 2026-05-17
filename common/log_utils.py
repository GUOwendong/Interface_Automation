#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""日志配置，基于 loguru，输出到控制台和文件"""
import sys

from loguru import logger

from config.global_config import LOGS_DIR

LOGS_DIR.mkdir(exist_ok=True)
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG",
)

log_file = LOGS_DIR / "interface_auto.log"

logger.add(
    str(log_file),
    rotation="10 MB",
    retention=7,
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
)
log = logger
