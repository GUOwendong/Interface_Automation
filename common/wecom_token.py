#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""企业微信 AccessToken 管理器（单例，自动缓存）"""
import time

import requests

from common.log_utils import log
from common.wecom_error_code import extract_error_from_response, is_success
from config.global_config import TIMEOUT, WECOM_CONFIG


class WeComTokenManager:
    _instance = None
    _token: str = None
    _expires_at: float = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_token(cls, force_refresh: bool = False) -> str:
        now = time.time()
        if not force_refresh and cls._token and now < cls._expires_at:
            log.debug("使用缓存的 access_token")
            return cls._token

        log.info("获取新的 access_token")
        url = f"{WECOM_CONFIG['base_url']}/cgi-bin/gettoken"
        params = {"corpid": WECOM_CONFIG["corp_id"], "corpsecret": WECOM_CONFIG["contact_secret"]}
        try:
            resp = requests.get(url, params=params, timeout=TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            log.error(f"请求 token 失败: {e}")
            raise RuntimeError(f"无法获取 access_token: {e}")

        if not is_success(data):
            error = extract_error_from_response(data)
            log.error(f"获取 token 业务失败: {error}")
            raise RuntimeError(f"获取 token 失败: {error}")

        cls._token = data["access_token"]
        expires_in = data.get("expires_in", 7200)
        cls._expires_at = now + expires_in - 60
        log.info(f"获取 token 成功，有效期 {expires_in} 秒")
        return cls._token

    @classmethod
    def refresh(cls) -> str:
        return cls.get_token(force_refresh=True)

    @classmethod
    def is_valid(cls) -> bool:
        return cls._token is not None and time.time() < cls._expires_at


def get_token() -> str:
    return WeComTokenManager.get_token()
