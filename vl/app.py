#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tornado.ioloop
import tornado.web

from vl.models import UserInformations

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
        user_informations = UserInformations.wrap(self.request.arguments)
        self.set_status(200)
        return self.write(user_informations.to_json())

def main():
    app = tornado.web.Application(
        [(r'/informations', InformationHandler)],
        debug=False,
        )
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
