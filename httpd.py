# -*- coding: UTF-8 -*-
# httpd.py

from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
import os
import sys

#reload(sys)
#sys.setdefaultencoding('euc-kr') 

os.chdir("c:\\httpd")
serv = HTTPServer(("", 1234), CGIHTTPRequestHandler)
serv.serve_forever()