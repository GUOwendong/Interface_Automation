#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""

from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests
from requests.exceptions import ConnectionError as ReqConnectionError
from requests.exceptions import RequestException, Timeout

from common.log_utils import log
from config.global_config import API_BASE_URL, TIMEOUT


class BaseApiClientError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[requests.Response] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class BaseApiClient:
    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = base_url or API_BASE_URL
        self.timeout = timeout or TIMEOUT
        self.session = requests.Session()
        self.log = log.bind(module=self.__class__.__name__)

        self.session.headers.update(
            {"User-Agent": "BaseApiClient/1.0", "Accept": "application/json", "Content-Type": "application/json"}
        )

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = urljoin(self.base_url.rstrip("/") + "/", path.lstrip("/"))

        try:
            resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
            self._check_status(resp)
            return resp
        except Timeout:
            self.log.error("Timeout: {} {}", method, url)
            raise
        except ReqConnectionError:
            self.log.error("Connection error: {} {}", method, url)
            raise
        except RequestException:
            self.log.exception("Request failed")
            raise

    def _check_status(self, resp: requests.Response):
        if not (200 <= resp.status_code < 300):
            raise BaseApiClientError(f"HTTP {resp.status_code}", status_code=resp.status_code, response=resp)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None):
        return self._request("GET", path, params=params)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None):
        return self._request("POST", path, json=json)

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
