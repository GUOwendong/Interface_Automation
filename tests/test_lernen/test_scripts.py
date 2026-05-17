#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: Conducting code practice and testing development work
"""
import requests


def test_requests():
    url = "https://httpbin.ceshiren.com/get"
    r = requests.request(method="GET", url=url)
    print(r.text)
    assert r.status_code == 200


def test_send_resume():
    url = "https://httpbin.ceshiren.com/post"
    resume = {
        "name": "guowendong",
        "gender": "male",
        "age": 20,
        "address": {"province": "Gansu", "city": "shenzhen", "street": "Nanjing Road", "number": 123},
        "skills": {
            "python": "熟练",
            "pytest": "熟练",
            "allure": "精通",
            "selenium": "熟练",
            "appium": "熟练",
            "jmeter": "精通",
        },
    }

    r = requests.post(url, data=resume)
    print(r.text)
    assert r.status_code == 200
    assert r.json()["form"]["name"] == "guowendong"
