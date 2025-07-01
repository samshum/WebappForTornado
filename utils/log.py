import logging
import os
import time
from logging.handlers import BaseRotatingHandler
from datetime import datetime

class NestedHourlyRotatingFileHandler(BaseRotatingHandler):
    """
    自定义日志处理器，实现以下功能:
    - 日志目录按 /年/月/日 嵌套创建
    - 日志文件按小时命名 (e.g., 00.log, 01.log, ..., 23.log)
    """
    def __init__(self, log_dir, encoding=None, delay=False, utc=False):
        self.log_dir = os.path.abspath(log_dir)
        self.utc = utc
        
        # 动态获取当前应写入的日志文件路径
        filename = self._get_current_filepath()
        super().__init__(filename, 'a', encoding, delay)
        
        # 计算下一次翻转时间 (下一个小时的开始)
        self.rolloverAt = self._compute_rollover(int(time.time()))

    def _get_current_filepath(self):
        """
        计算并返回当前的日志文件路径，如果目录不存在则创建。
        路径格式: /path/to/logs/YYYY/MM/DD/HH.log
        """
        if self.utc:
            now = datetime.utcnow()
        else:
            now = datetime.now()
        
        # 构建目录路径
        date_dir = os.path.join(self.log_dir, now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'))
        # 创建嵌套目录
        os.makedirs(date_dir, exist_ok=True)
        
        # 返回完整的文件路径
        return os.path.join(date_dir, f"{now.strftime('%H')}.log")

    def _compute_rollover(self, currentTime):
        """计算下一个翻转时间点 (下一个小时的整数点)"""
        return (currentTime // 3600 + 1) * 3600

    def shouldRollover(self, record):
        """判断是否需要翻转日志文件"""
        t = int(time.time())
        return 1 if t >= self.rolloverAt else 0

    def doRollover(self):
        """
        执行翻转。关闭当前文件流，并基于当前时间创建新的文件流。
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        
        # 获取新的文件路径并设置为基准文件名
        self.baseFilename = self._get_current_filepath()
        self.stream = self._open()
        
        # 计算下一次翻转时间
        self.rolloverAt = self._compute_rollover(int(time.time()))

def setup_logger():
    """
    配置并返回一个 logger 实例。
    """
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
    
    # 使用一个固定的名称获取 logger
    log = logging.getLogger('app')
    log.setLevel(logging.INFO)

    # 防止重复添加 handler
    if not log.handlers:
        handler = NestedHourlyRotatingFileHandler(log_dir)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)

    return log

# 创建并导出 log 实例
log = setup_logger()
