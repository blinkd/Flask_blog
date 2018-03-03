#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname
import app


sys.path.insert(0, abspath(dirname(__file__)))
application = app.configured_app()

"""
建立一个软连接
ln -s /var/www/bbs/web.conf /etc/supervisor/conf.d/web.conf

ln -s /var/www/bbs/web.nginx /etc/nginx/sites-enabled/bbs



➜  ~ cat /etc/supervisor/conf.d/web.conf

[program:bbs]
command=/usr/local/bin/gunicorn wsgi -c gunicorn.config.py
directory=/var/www/bbs
autostart=true
autorestart=true


"""
