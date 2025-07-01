# -*- coding: utf-8 -*-

import os
import importlib
import inspect
import tornado.web

def auto_generate_routes():
    """
    自动扫描handlers目录，根据文件夹和文件名生成路由
    """
    routes = []
    handlers_dir = os.path.join(os.path.dirname(__file__), 'handlers')
    
    # 遍历handlers目录
    for root, dirs, files in os.walk(handlers_dir):
        for file in files:
            # 只处理Python文件，排除__init__.py和其他非Python文件
            if file.endswith('.py') and file != '__init__.py':
                # 获取相对路径
                rel_path = os.path.relpath(root, handlers_dir)
                # 获取模块名
                module_name = os.path.splitext(file)[0]
                
                # 构建完整的模块路径
                if rel_path == '.':
                    full_module_path = f'handlers.{module_name}'
                    url_path = f'/{module_name}' if module_name != 'index' else '/'
                else:
                    rel_path = rel_path.replace(os.path.sep, '.')
                    full_module_path = f'handlers.{rel_path}.{module_name}'
                    url_path = f'/{rel_path}/{module_name}' if module_name != 'index' else f'/{rel_path}'
                
                try:
                    # 动态导入模块
                    module = importlib.import_module(full_module_path)
                    
                    # 查找模块中的Handler类
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            name == 'Handler' and
                            issubclass(obj, tornado.web.RequestHandler)):
                            routes.append((url_path, obj))
                            break
                except ImportError as e:
                    print(f"Error importing {full_module_path}: {e}")
    
    return routes

# 自动生成路由
router = auto_generate_routes()

# 打印生成的路由，用于调试
print("Generated routes:")
for route in router:
    print(f"  {route[0]} -> {route[1].__module__}.{route[1].__name__}")