#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Contact       : yidacai@foxmail.com
@Created       : 2023/04/18 09:23:05
@Description   :
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
"""
from controller import Controller

import abc
import json

import tornado.web
from tornado import gen
from tornado.web import HTTPError
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

import datetime

import logging
import traceback
import time
import uuid

import random


logger = logging.getLogger()
NUMBER_OF_EXECUTOR = 6


"""
handler --- post方法测试
400错误是参数与控制器层所需要的参数不符合。
500错误是传入的参数在业务处理中出现了异常。
"""


class BasePostRequestHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(NUMBER_OF_EXECUTOR)
    request_timeout = 10

    @gen.coroutine
    def post(self, *args, **kwargs):
        request_id = str(uuid.uuid4())
        try:
            result = yield gen.with_timeout(
                datetime.timedelta(seconds=self.request_timeout),
                self._post(request_id, *args, **kwargs),
                quiet_exceptions=gen.TimeoutError,
            )
            self.write(result)
        except gen.TimeoutError:
            self.set_status(500)
            self.write({"msg": "Request timeout"})
        except HTTPError as e:
            logger.error(traceback.format_exc())
            self.set_status(e.status_code)
            self.write({"msg": e.log_message})
        except Exception as e:
            traceback.print_exc()
            logger.error(traceback.format_exc())
            self.set_status(500)
            self.write({"msg": "Internal server error"})
        finally:
            self.finish()

    @run_on_executor
    def _post(self, request_id, *args, **kwargs):
        request = self._post_request_arguments(request_id, *args, **kwargs)
        res = self._request_service(request_id, **request)
        return res

    @abc.abstractmethod
    def _post_request_arguments(self, *args, **kwargs):
        # NotImplementedError: intended to remind developers to implement the abstract method in the subclass.
        raise NotImplementedError(
            "call to abstract method %s._get_request_arguments" % self.__class__
        )

    @abc.abstractmethod
    def _request_service(self, **kwargs):
        raise NotImplementedError(
            "call to abstract method %s._request_service" % self.__class__
        )


class PostHandler(BasePostRequestHandler):
    def _post_request_arguments(self, request_id, *args, **kwargs):
        """
        获取数据
        :param args:
        :param kwargs:
        :return:
        """

        data = json.loads(self.request.body)
        logger.info(f"request - {request_id} - {data}")
        if not data:
            raise HTTPError(400, "Query argument cannot be empty string")
        return data

    def _request_service(self, request_id, **kwargs):
        """
        处理数据
        :param kwargs:
        :return:
        """
        if kwargs:
            time.sleep(random.randint(1, 8))
            controller = Controller(kwargs)
            res = controller.run()
            logger.info(f"respone - {request_id} - {res}")
        else:
            raise HTTPError(400, "Query argument cannot be empty string")
        return res
