#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Contact       : yidacai@foxmail.com
@Created       : 2023/04/18 09:40:27
@Description   :
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
"""

class Controller(object):
    """
    控制层业务举例
    """

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def run(self):
        return self.kwargs
