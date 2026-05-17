#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""

import os

import pytest
import requests

from common.file_utils import FileUtil
from common.wecom_token import get_token
from config.global_config import DATA_DIR

token = get_token()

dept_data = FileUtil.read_excel("xlsx/create_department.xlsx")


@pytest.mark.parametrize("case", dept_data, ids=lambda x: x["case_id"])
def test_creat_department(case):
    url = "https://qyapi.weixin.qq.com/cgi-bin/department/create"
    params = {"access_token": token}

    body = {
        "name": case["name"],
        "name_en": case["name_en"],
        "parentid": case["parentid"],  # noqa
        "order": case["order"],
        "id": case["id"],
    }

    response = requests.post(url=url, params=params, json=body)

    assert response.status_code == 200, f"请求失败，状态码：{response.status_code}"
    assert (
        response.json()["errcode"] == case["errcode"]
    ), f"❌ 创建部门失败 | 错误码：{response.json()["errcode"]} | 原因：{response.json()["errmsg"]}"
