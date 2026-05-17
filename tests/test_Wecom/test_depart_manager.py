#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""

import allure
import pytest

from common.api_client import ApiClient
from common.wecom_token import get_token


@pytest.fixture(scope="module")
def api_client():
    """提供已注入 token 的 ApiClient 实例"""
    client = ApiClient()
    token = get_token()
    client.set_access_token(token)  # noqa
    yield client
    client.close()


@allure.feature("部门管理")
class TestDepartment:

    @allure.story("创建部门")
    @pytest.mark.smoke
    def test_creat_department(self, api_client):
        """创建部门"""
        path = "/cgi-bin/department/create"
        body = {"name": "广州研发中心", "parentid": 1, "id": 111111}
        with allure.step("发送创建部门请求"):
            response = api_client.post_json(path, json=body)

        with allure.step("验证响应"):
            assert (
                response["errcode"] == 0
            ), f"❌ 创建部门失败 | 错误码：{response['errcode']} | 原因：{response.get('errmsg', '')}"

    @allure.story("更新部门")
    @pytest.mark.smoke
    def test_update_department(self, api_client):
        """更新部门"""
        path = "/cgi-bin/department/update"
        body = {"id": 111111, "name": "地球研发中心"}
        with allure.step("发送更新部门请求"):
            response = api_client.post_json(path, json=body)

        with allure.step("验证响应"):
            assert (
                response["errcode"] == 0
            ), f"❌ 更新部门失败 | 错误码：{response['errcode']} | 原因：{response.get('errmsg', '')}"

    @allure.story("删除部门")
    @pytest.mark.smoke
    def test_delete_department(self, api_client):
        """删除部门"""
        path = "/cgi-bin/department/delete"
        params = {"id": 111111}
        with allure.step("发送删除部门请求"):
            response = api_client.get_json(path, params=params)

        with allure.step("验证响应"):
            assert (
                response["errcode"] == 0
            ), f"❌ 删除部门失败 | 错误码：{response['errcode']} | 原因：{response.get('errmsg', '')}"

    @allure.story("查询部门列表")
    @pytest.mark.smoke
    def test_list_departments(self, api_client):
        """获取部门列表"""
        path = "/cgi-bin/department/list"
        with allure.step("发送查询部门列表请求"):
            response = api_client.get_json(path)

        with allure.step("验证响应"):
            assert (
                response["errcode"] == 0
            ), f"❌ 查询部门列表失败 | 错误码：{response['errcode']} | 原因：{response.get('errmsg', '')}"
            assert "department" in response
