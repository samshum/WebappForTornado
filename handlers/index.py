
from base import RequestHandler


class Handler(RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        self.render("index.html")

    def put(self):
        self.render("index.html")

    def delete(self):
        self.render("index.html")