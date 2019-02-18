#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import tornado.ioloop
import tornado.web

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from facereg import google_images

try:
    from collections.abc import defaultdict, Mapping, namedtuple
except ImportError:
    from collections import defaultdict, Mapping, namedtuple

try:
    scheme = os.environ['SCHEME']
    ip_address = os.environ['IP_ADDRESS']
    port = os.environ['PORT']
    max_workers = os.environ['MAX_WORKERS']
except KeyError:
    scheme = 'http'
    ip_address = 'localhost'
    port = 80
    max_workers = 8

class InformationHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(max_workers=max_workers)
    json_model = ['name', 'surname', 'gender',
            'date_of_birth', 'place_of_birth', 'country']

    def __validate_json(self, arguments):
        if set(arguments.keys()) != set(self.json_model):
            return False
        for key in self.json_model:
            if arguments[key] == None:
                return False
        return True

    @run_on_executor
    def __download_images(self, name, surname):
        output_directory = os.getcwd() + '/datasets'
        _, _ = google_images.download(str.format('{0} {1}', name, surname),
                                limit=3, output_directory=output_directory)

    @tornado.gen.coroutine
    def post(self):
        if self.__validate_json(self.request.arguments) == False:
            self.set_status(400)
            response = {
                'error': True,
                'message': 'Missing values'
                }
            return self.write(json.dumps(response, sort_keys=True))
        else:
            yield self.__download_images(self.get_argument('name'), self.get_argument('surname'))
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
