#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTTP 客户端封装，支持自定义异常、自动 token（适配企业微信）"""

from typing import Optional
from urllib.parse import urljoin

import requests
from requests.exceptions import ConnectionError as ReqConnectionError
from requests.exceptions import RequestException, Timeout

from common.log_utils import log
from config.global_config import API_BASE_URL, TIMEOUT


class ApiClientError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[requests.Response] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response

    def __str__(self):
        return f"[{self.status_code}] {self.message}" if self.status_code else self.message


class ApiTimeoutError(ApiClientError):
    pass


class ApiConnectionError(ApiClientError):
    pass


class ApiHttpError(ApiClientError):
    pass


class ApiAuthError(ApiClientError):
    pass


class ApiNotFoundError(ApiClientError):
    pass


class ApiResponseError(ApiClientError):
    pass


class ApiClient:
    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = base_url or API_BASE_URL
        self.access_token = None
        self.timeout = timeout or TIMEOUT
        self.session = requests.Session()
        self.log = log.bind(module="api_client")
        self.session.headers.update(
            {"User-Agent": "ApiClient/1.0", "Accept": "application/json", "Content-Type": "application/json"}
        )

    def set_access_token(self, token: str):
        """设置企业微信 access_token（会添加到 URL 参数）"""
        self.access_token = token

    def _request(self, method: str, path: str, raise_for_status: bool = True, **kwargs) -> requests.Response:
        url = urljoin(self.base_url.rstrip("/") + "/", path.lstrip("/"))

        # 自动注入 access_token 到 url 参数
        if self.access_token:
            params = dict(kwargs.get("params", {}))
            params.setdefault("access_token", self.access_token)
            kwargs["params"] = params
        else:
            self.log.debug("access_token is None!")

        try:
            resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
            if raise_for_status:
                self._check_status(resp)
            return resp
        except Timeout:
            self.log.error(f"Timeout: {method} {url}")
            raise ApiTimeoutError(f"请求超时 {self.timeout}s", status_code=408)
        except ReqConnectionError:
            self.log.error(f"Connection error: {method} {url}")
            raise ApiConnectionError(f"连接失败: {url}")
        except RequestException as e:
            self.log.error(f"Request failed: {method} {url}, error: {e}")
            raise ApiHttpError(str(e), status_code=getattr(e.response, "status_code", None))

    def _check_status(self, resp: requests.Response):
        if 200 <= resp.status_code < 300:
            return
        if resp.status_code == 401:
            raise ApiAuthError("认证失败", status_code=401, response=resp)
        if resp.status_code == 404:
            raise ApiNotFoundError("资源不存在", status_code=404, response=resp)
        try:
            error_msg = resp.json().get("message", resp.text[:200])
        except:
            error_msg = resp.text[:200]
        raise ApiHttpError(error_msg, status_code=resp.status_code, response=resp)

    def _check_wecom_response(self, data: dict):
        if not isinstance(data, dict):
            raise ApiResponseError("Invalid response type")
        errcode = data.get("errcode", 0)
        if errcode != 0:
            raise ApiAuthError(f"wecom error: {data.get('errmsg')}", status_code=errcode)

    def get(self, path: str, params=None, headers=None, raise_for_status=True):
        return self._request("GET", path, params=params, headers=headers, raise_for_status=raise_for_status)

    def post(self, path: str, data=None, json=None, headers=None, raise_for_status=True):
        return self._request("POST", path, data=data, json=json, headers=headers, raise_for_status=raise_for_status)

    def put(self, path: str, json=None, headers=None, raise_for_status=True):
        return self._request("PUT", path, json=json, headers=headers, raise_for_status=raise_for_status)

    def delete(self, path: str, headers=None, raise_for_status=True):
        return self._request("DELETE", path, headers=headers, raise_for_status=raise_for_status)

    def patch(self, path: str, json=None, headers=None, raise_for_status=True):
        return self._request("PATCH", path, json=json, headers=headers, raise_for_status=raise_for_status)

    def get_json(self, path: str, params=None, headers=None):
        resp = self.get(path, params=params, headers=headers)
        data = self._parse_json(resp)
        self._check_wecom_response(data)
        return data

    def post_json(self, path: str, json=None, headers=None):
        resp = self.post(path, json=json, headers=headers)
        data = self._parse_json(resp)
        self._check_wecom_response(data)
        return data

    def _parse_json(self, resp: requests.Response):
        if not resp.content:
            return None
        try:
            return resp.json()
        except Exception as e:
            raise ApiResponseError(f"JSON 解析失败: {e}, raw={resp.text[:200]}", status_code=resp.status_code)

    def set_header(self, key: str, value: str):
        self.session.headers.update({key: value})

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
