from base import RequestHandler
from utils.log import log


class NotFoundHandler(RequestHandler):
    """处理404错误的处理程序"""
    
    def prepare(self):
        self.set_status(404)
        log.error(f"E404: Page not found at {self.request.uri}")
        self.render("error.html", status_code=404, error_message="页面未找到")
    
    def get(self, *args, **kwargs):
        pass
        
    def post(self, *args, **kwargs):
        pass