#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import tornado.ioloop
import tornado.web

try:
    scheme = os.environ['SCHEME']
    ip_address = os.environ['IP_ADDRESS']
    port = os.environ['PORT']
except KeyError:
    scheme = 'http'
    ip_address = 'localhost'
    port = 80

class InformationHandler(tornado.web.RequestHandler):

    json_model = ['name', 'surname', 'sex',
            'date_of_birth', 'place_of_birth', 'country']

    def __validate_json(self, arguments):
        return set(arguments.keys()) == set(self.json_model)

    def post(self):
        if self.__validate_json(self.request.arguments) == False:
            self.set_status(400)
            response = {
                'error': True,
                'message': 'Missing values'
                }
            return self.write(json.dumps(response, sort_keys=True))
        else:
            self.set_status(200)
            response = {
                'error': False,
                'message': 'Values received!'
                }
            return self.write(json.dumps(response, sort_keys=True))

def main():
    app = tornado.web.Application(
        [(r'/informations', InformationHandler)],
        debug=False,
        )
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
