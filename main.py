#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: 测试执行入口，支持环境切换
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from common.log_utils import log
from config.global_config import ALLURE_REPORT_DIR, ALLURE_RESULTS_DIR, Env


def run_tests(env: str = "test") -> bool:
    os.environ["TEST_ENV"] = env
    log.info(f"开始运行测试，环境: {env}")

    pytest_cmd = ["pytest", "-v", "-s"]
    log.info(f"执行: {' '.join(pytest_cmd)}")
    pytest_result = subprocess.run(pytest_cmd)

    if pytest_result.returncode != 0:
        log.error(f"pytest 失败，返回码: {pytest_result.returncode}")
        tests_failed = True
    else:
        log.info("pytest 成功")
        tests_failed = False

    if ALLURE_RESULTS_DIR.exists():
        allure_cmd = ["allure", "generate", str(ALLURE_RESULTS_DIR), "-o", str(ALLURE_REPORT_DIR), "--clean"]
        log.info(f"生成 Allure 报告: {' '.join(allure_cmd)}")
        subprocess.run(allure_cmd)
    else:
        log.warning(f"Allure 结果目录不存在: {ALLURE_RESULTS_DIR}")

    return not tests_failed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", choices=[e.value for e in Env], default="test", help="测试环境")
    args = parser.parse_args()
    success = run_tests(env=args.env)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
