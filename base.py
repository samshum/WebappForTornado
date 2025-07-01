# -*- coding: utf-8 -*-

import tornado.web
from utils.log import log


class RequestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.set_header("X-Content-Type-Options", "nosniff")
        self.set_header("X-Frame-Options", "DENY")
        self.set_header("X-XSS-Protection", "1; mode=block")
        # 仅在HTTPS环境下启用HSTS
        self.set_header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        # Content-Security-Policy 需要根据实际情况配置，这里提供一个基本示例
        self.set_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'")

    def write_error(self, status_code, **kwargs):
        log.error(f"E{status_code}: {self._reason}")
        self.render("error.html", status_code=status_code, message=self._reason)
