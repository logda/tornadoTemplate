import contextvars
import logging
import uuid

import tornado.ioloop
import tornado.web
import random
import time

logger = logging.getLogger(__name__)
request_id_var = contextvars.ContextVar("request_id")


# Let's have an async function for the sake of demonstration
async def generate_number():
    time.sleep(random.randint(1, 8))
    return 4


class MyHandler(tornado.web.RequestHandler):
    # prepare is called at the beginning of request handling
    def prepare(self):
        # If the request headers do not include a request ID, let's generate one.
        request_id = self.request.headers.get("request-id") or str(uuid.uuid4())
        request_id_var.set(request_id)

    async def get(self):
        logger.info('request')
        number = await generate_number()
        logger.info('respone')
        self.write(f"Here's a number: {number}")


def make_app():
    return tornado.web.Application([(r"/", MyHandler),])


class MyFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_var.get("-")
        return True


if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)s %(request_id)s %(message)s", level=logging.INFO
    )

    # Log filters do not propagate, but handlers do. Thus we add the filter
    # to the handlers of the root logger so that the messages of child loggers
    # get filtered as well.
    my_filter = MyFilter()
    for handler in logging.getLogger().handlers:
        handler.addFilter(my_filter)

    port = 8000
    app = make_app()
    app.listen(port)
    logger.info("Listening at http://localhost:%d/", port)
    tornado.ioloop.IOLoop.current().start()