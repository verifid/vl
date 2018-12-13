#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tornado.ioloop
import tornado.web
import json

try:
    scheme = os.environ['SCHEME']
    ip_address = os.environ['IP_ADDRESS']
    port = os.environ['PORT']
except KeyError:
    scheme = 'http'
    ip_address = 'localhost'
    port = 80

class InformationHandler(tornado.web.RequestHandler):

    def post(self):
        infomations = json.dumps({ k: self.get_argument(k) for k in self.request.arguments }, sort_keys=True)
        self.set_status(200)
        return self.write(infomations)

def main():
    app = tornado.web.Application(
        [(r'/informations', InformationHandler)],
        debug=False,
        )
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
