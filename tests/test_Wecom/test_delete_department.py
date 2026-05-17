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


@pytest.mark.parametrize("deptid", dept_data, ids=lambda x: x["case_id"])
def test_delete_department(deptid):
    url = "https://qyapi.weixin.qq.com/cgi-bin/department/delete"
    params = {"access_token": token, "id": deptid["id"]}
    response = requests.get(url=url, params=params)

    assert response.status_code == 200, f"实际响应状态码：{response.status_code}"
    assert (
        response.json()["errcode"] == deptid["errcode"]
    ), f"❌ 删除部门失败 | 错误码：{response.json()["errcode"]} | 原因：{response.json()["errmsg"]}"
