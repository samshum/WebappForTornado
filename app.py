# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
from tornado.options import define, options

import config
from base import RequestHandler
from router import router
from handlers.error import NotFoundHandler

define("port", default=config.port, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            debug=config.debug,
            static_path="static",
            template_path="templates",
            default_handler_class=NotFoundHandler
        )
        super(Application, self).__init__(router, **settings)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    print(f"Server is running on http://127.0.0.1:{options.port}")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()