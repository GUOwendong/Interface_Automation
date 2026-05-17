#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: pytest 全局配置：夹具、失败截图（根目录）
"""

import pytest

from common.api_client import ApiClient
from common.log_utils import log
from common.wecom_token import get_token
from config.global_config import SCREENSHOTS_DIR


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def api_client():
    client = ApiClient()
    token = get_token()
    client.set_access_token(token)
    log.info("✅ 全局 ApiClient 已初始化，Token 已注入")
    yield client
    client.close()
    log.info("全局 ApiClient 已关闭")


@pytest.fixture(autouse=True)
def auto_failure_snapshot(request):
    """测试失败时自动保存快照到 SCREENSHOTS_DIR"""
    yield
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        safe_name = request.node.name.replace("/", "_").replace("\\", "_")
        snapshot_file = SCREENSHOTS_DIR / f"{safe_name}.txt"
        with open(snapshot_file, "w", encoding="utf-8") as f:
            f.write(f"Test Failed: {request.node.name}\n")
            f.write(f"Node ID: {request.node.nodeid}\n")
            f.write(f"Location: {request.node.location}\n")
        log.error(f"❌ 用例失败: {request.node.name}，快照已保存: {snapshot_file}")
