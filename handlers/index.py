
from base import RequestHandler


class Handler(RequestHandler):
    def get(self):
        self.render("index.html")