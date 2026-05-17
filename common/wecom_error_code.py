#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""企业微信错误码映射"""
from enum import IntEnum
from typing import Any, Dict, Optional

from common.log_utils import log


class WeComErrorCode(IntEnum):
    SUCCESS = 0
    INVALID_TOKEN = 40001
    MISSING_TOKEN = 41001
    INVALID_PARTY_ID = 60123
    PARENT_DEPT_NOT_FOUND = 60004
    INVALID_CREDENTIAL = 40013
    ACCESS_TOKEN_EXPIRED = 42001
    USER_NOT_FOUND = 60111


ERROR_MSG: Dict[int, str] = {
    0: "成功",
    40001: "无效的 access_token",
    40013: "无效的 corpid 或 secret",
    41001: "缺少 access_token",
    42001: "access_token 已过期",
    60004: "父部门不存在",
    60111: "用户不存在",
    60123: "无效的部门 ID",
}


def get_error_message(code: int) -> str:
    msg = ERROR_MSG.get(code)
    if msg is None:
        log.warning(f"未知错误码: {code}")
        return f"未知错误({code})"
    return msg


def extract_error_from_response(resp_data: Dict[str, Any]) -> Optional[str]:
    errcode = resp_data.get("errcode")
    if errcode is None or errcode == 0:
        return None
    errmsg = resp_data.get("errmsg", "")
    if not errmsg or errmsg == "unknown error":
        errmsg = get_error_message(errcode)
    return f"[{errcode}] {errmsg}"


def is_success(resp_data: Dict[str, Any]) -> bool:
    return resp_data.get("errcode") == 0
