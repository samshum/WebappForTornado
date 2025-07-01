# -*- coding: utf-8 -*-
import os

# server
port = 8082
debug = bool(os.environ.get('debug', 'false'))

# To enable debug mode in development, set the environment variable DEBUG_MODE to 'True'
# For example: DEBUG_MODE=True python app.py