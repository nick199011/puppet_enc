#!/usr/bin/python

import tornado.ioloop
import tornado.web
import tornado.httpserver
import ruamel.yaml
import os
import sys
import tornado.options

from tornado.options import options, define
define("port",default=8888,help="running on 8888",type=int)

if not os.environ.has_key('_BASIC_PATH_'):
    _BASIC_PATH_ = os.path.abspath(__file__)
    _BASIC_PATH_ = _BASIC_PATH_[:_BASIC_PATH_.rfind('/bin/')]
    os.environ['_BASIC_PATH_'] = _BASIC_PATH_

if sys.path.count(os.environ['_BASIC_PATH_'] + '/lib') == 0:
    sys.path.append(os.environ['_BASIC_PATH_'] + '/lib')

settings = {
    "static_path" : os.path.join(os.environ['_BASIC_PATH_'],"static"),
    "template_path" : os.path.join(os.environ['_BASIC_PATH_'],"template"),
    "debug" : False,
}

print settings
from db import mydb 

dic={'classes':{},'parameters': {'path':'/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin','puppetserver':'puppet.500boss.com'},'environment':'production'}
#yam="""
#classes: 
#  nginx_new:
#parameters:
#  host: news_int
#"""

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        puppet_db=mydb()
        node=self.get_argument('node')
        r=puppet_db.getnodeclass(node.replace('.500x.com',''))
        #r=puppet_db.getnodeclass(node)
        self.write(r)

class AdminHandler(tornado.web.RequestHandler):
    def get(self,filename):
        #logger.debug('testtest')
        #self.write('testtest')
        #print who
        self.render(filename)

class TableHandler(tornado.web.RequestHandler):
    def get(self):
        #logger.debug('testtest')
        #self.write('testtest')
        #print who
        puppet_db=mydb()
        #machines=puppet_db.get_machine_list()
        #self.render("tables.html",machines=({'hostname':'dddd','ip':'testet'},{'hostname':'dfdaf','ip':'etwqtq'}))
        self.render("tables.html",machines=puppet_db.get_machine_list(),all_node_groups=puppet_db.get_all_node_groups())
        

class ApiAddnode(tornado.web.RequestHandler):
    def post(self):
        #logger.debug('testtest')
        hostname=self.get_argument('hostname')
        node_group=self.get_argument('node_group')
        self.write(hostname+node_group)
        #print who


application = tornado.web.Application(
[
    (r"/",MainHandler),(r"/pages/tables.html",TableHandler),(r"/pages/(.*)",AdminHandler),(r"/api/add_node",ApiAddnode)
],**settings
)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(options.port)
    http_server.start(0)
    tornado.ioloop.IOLoop.instance().start()


