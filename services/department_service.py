#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""企业微信部门服务封装"""
from typing import Any, Dict, Optional

from common.api_client import ApiClient
from common.log_utils import log
from common.wecom_error_code import extract_error_from_response, is_success
from common.wecom_token import get_token


class DepartmentService:
    def __init__(self, base_url: str = "https://qyapi.weixin.qq.com"):
        self.client = ApiClient(base_url=base_url)
        self._token = None

    def _ensure_token(self):
        if self._token is None:
            self._token = get_token()
            self.client.set_auth_token(self._token)

    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        self._ensure_token()
        if method.upper() == "GET":
            resp = self.client.get_json(path, **kwargs)
        elif method.upper() == "POST":
            resp = self.client.post_json(path, **kwargs)
        else:
            raise ValueError(f"不支持的方法: {method}")
        if not is_success(resp):
            error = extract_error_from_response(resp)
            log.error(f"企业微信 API 错误: {error}")
            raise RuntimeError(f"部门服务调用失败: {error}")
        return resp

    def create(self, name: str, parentid: int = 1, dept_id: int = None) -> Dict:
        path = "/cgi-bin/department/create"
        body = {"name": name, "parentid": parentid}
        if dept_id:
            body["id"] = dept_id
        return self._request("POST", path, json=body)

    def update(self, dept_id: int, name: str = None, parentid: int = None) -> Dict:
        path = "/cgi-bin/department/update"
        body = {"id": dept_id}
        if name:
            body["name"] = name
        if parentid:
            body["parentid"] = parentid
        return self._request("POST", path, json=body)

    def delete(self, dept_id: int) -> Dict:
        path = "/cgi-bin/department/delete"
        return self._request("GET", path, params={"id": dept_id})

    def list(self, parent_id: int = None) -> Dict:
        path = "/cgi-bin/department/list"
        params = {}
        if parent_id:
            params["id"] = parent_id
        return self._request("GET", path, params=params)
