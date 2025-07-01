
from base import RequestHandler


class Handler(RequestHandler):
    def get(self):
        self.render("use.html", title="Use Page", message="This is the use page content.")