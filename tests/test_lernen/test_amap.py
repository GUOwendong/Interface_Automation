#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""

import requests


def test_amap():
    url = "https://httpbin.ceshiren.com/get"
    args = {}

    response = requests.get(url, params=args)
    print(response.json())

    assert response.status_code == 200
    assert response.json()["args"] == {}
