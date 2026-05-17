#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全局配置：路径、环境、API 地址、超时等"""
import os
from enum import Enum
from pathlib import Path

# ==================== 项目路径 ====================
# 取当前文件的绝对路径，.parent回退到上一级，回到项目根目录下
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
REPORTS_DIR = BASE_DIR / "reports"
ALLURE_RESULTS_DIR = REPORTS_DIR / "allure-results"
ALLURE_REPORT_DIR = REPORTS_DIR / "allure-report"

# 自动创建必要目录
for d in [LOGS_DIR, SCREENSHOTS_DIR, ALLURE_RESULTS_DIR, ALLURE_REPORT_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ===================== 环境配置 ====================
class Env(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


CURRENT_ENV = Env(os.getenv("TEST_ENV", "test"))

# API 基础地址（按环境区分）
API_BASE_URL_MAP = {
    Env.DEV: "http://127.0.0.1:8000",
    Env.TEST: "https://qyapi.weixin.qq.com",
    Env.PROD: "https://qyapi.weixin.qq.com",
}
API_BASE_URL = API_BASE_URL_MAP[CURRENT_ENV]
TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# 企业微信配置（从环境变量读取，避免硬编码）
WECOM_CONFIG = {
    "corp_id": os.getenv("WECOM_CORP_ID", "your_corp_id"),
    "contact_secret": os.getenv("WECOM_CONTACT_SECRET", "your_secret"),
    "base_url": "https://qyapi.weixin.qq.com",
}
