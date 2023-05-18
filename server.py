#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Contact       : yidacai@foxmail.com
@Created       : 2023/04/18 09:19:31
@Description   :
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
"""

import tornado.web
from tornado.web import URLSpec
from tornado.ioloop import IOLoop
import logging

from handler import PostHandler


import logging


import logging.config

logging.config.fileConfig("log.conf")
logger = logging.getLogger()


HANDLERS = [URLSpec(r"/example", PostHandler, name=PostHandler.__name__)]

if __name__ == "__main__":
    SERVER_PORT = 9313
    app = tornado.web.Application(handlers=HANDLERS, debug=True)
    app.listen(SERVER_PORT)
    logger.info(
        "Clean Panel server started on port {SERVER_PORT}".format(
            SERVER_PORT=SERVER_PORT
        )
    )
    IOLoop.current().start()
