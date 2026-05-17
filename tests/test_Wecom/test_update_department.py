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

yaml_data = FileUtil.read_yaml("yaml/update_department.yaml")


@pytest.mark.parametrize("dept", yaml_data, ids=lambda x: x["case_id"])
def test_update_department(dept):
    url = "https://qyapi.weixin.qq.com/cgi-bin/department/update"
    params = {"access_token": token}
    body = {
        "id": dept["id"],
        "name": dept["name"],
        "name_en": dept["name_en"],
        "parentid": dept["parentid"],
        "order": dept["order"],
    }
    response = requests.post(url=url, params=params, json=body)

    assert response.status_code == 200, f"实际响应状态码：{response.status_code}"
    assert (
        response.json()["errcode"] == 0
    ), f"❌ 更新部门失败 | 错误码：{response.json()["errcode"]} | 原因：{response.json()["errmsg"]}"
