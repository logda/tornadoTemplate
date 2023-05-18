#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Contact       : yidacai@foxmail.com
@Created       : 2023/03/30 11:23:20
@Description   :
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
"""


from unittest import TestCase
import requests
import json
import unittest
import requests


class TestPostHandler(TestCase):
    API_URL = "http://localhost:9313/example"
    proxies = {
        "http": None,
        "https": None,
    }

    def test_example_1(self):
        payload = {
            "explain": ["SELECT * FROM users WHERE age > 25"],
            "analyze": "SELECT * FROM users WHERE age > 25",
            "analyze_values": ["25"],
            "sql": "SELECT * FROM users WHERE age > 25",
            "map": {},
        }
        json_data = json.dumps(payload)
        resp = requests.post(self.API_URL, json_data,proxies=self.proxies)
        print(resp.json())


if __name__ == "__main__":
    unittest.main(verbosity=2)
