#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import tornado.ioloop
import tornado.web
import tornado.httpserver
import logging
import uuid

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from facereg import google_images
from urllib.parse import urlparse
from redis import Redis
from vl.redis_store import RedisStore
from enum import Enum

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
    port = 5000
    max_workers = 8

redis = Redis(host='localhost', port=6379)
store = RedisStore(redis)

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")

class UserDataHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(max_workers=max_workers)
    json_model = ['name', 'surname', 'gender',
            'date_of_birth', 'place_of_birth', 'country']

    def __validate_json(self, json_object):
        if set(json_object.keys()) != set(self.json_model):
            return False
        for key in self.json_model:
            if json_object[key] == None:
                return False
        return True

    def __uuid(self):
        return str(uuid.uuid4())

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    @run_on_executor
    def __download_images(self, name, surname, user_id):
        output_directory = os.getcwd() + '/datasets/' + user_id
        _, _ = google_images.download(str.format('{0} {1}', name, surname),
                                limit=3, output_directory=output_directory)

    @tornado.gen.coroutine
    def post(self):
        json_object = json.loads(self.request.body.decode('utf-8'))
        if self.__validate_json(json_object) == False:
            self.set_status(400)
            response = {
                'error': True,
                'message': 'Missing values'
                }
            return self.write(json.dumps(response, sort_keys=True))
        else:
            uuid = self.__uuid()
            yield self.__download_images(json_object['name'], json_object['surname'], uuid)
            store.keep(uuid, self.request.body)
            self.set_status(200)
            response = {
                'error': False,
                'message': 'Values received!',
                'userId': uuid
                }
            return self.write(json.dumps(response, sort_keys=True))

class UploadImageHandler(tornado.web.RequestHandler):

    class ValidationError(Enum):
        MISSING_DATA = 1
        NO_USER_FOUND = 2
        USER_FOUND = 3

        def read_response(self, argument):
            switcher = {
                1: (400, {'error': True,
                    'message': 'No user id found on request.'}),
                2: (200, {'error': True,
                    'message': 'No user found with given id.'}),
                3: (200, {'error': False,
                    'message': 'User found with given id.'})
            }
            return switcher.get(argument, "Invalid argument")

        def __str__(self):
            return self.read_response(self._value_)

    def __validate_arguments(self, arguments):
        if 'userId' not in arguments:
            return UploadImageHandler.ValidationError.MISSING_DATA
        user_id = arguments.get('userId')
        if isinstance(user_id, list):
            user_id = user_id[0].decode('utf-8')
        if store.value_of(user_id) == None:
            return UploadImageHandler.ValidationError.NO_USER_FOUND
        return UploadImageHandler.ValidationError.USER_FOUND

    def post(self):
        validation_error = self.__validate_arguments(self.request.arguments)
        if validation_error != UploadImageHandler.ValidationError.USER_FOUND:
            status_code, response = validation_error.__str__()
            self.set_status(status_code)
            return self.write(json.dumps(response, sort_keys=True))    
        if len(self.request.files) == 0:
            response = {
                'error': True,
                'message': 'No files found.'
                }
            self.set_status(412)
            return self.write(json.dumps(response, sort_keys=True))    
        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info["filename"], info["content_type"]
                body = info["body"]
                logging.info(
                    'POST "%s" "%s" %d bytes', filename, content_type, len(body)
                )
        self.set_status(200)
        response = {
            'error': False,
            'message': 'Image file received!'
            }
        return self.write(json.dumps(response, sort_keys=True))

def create_app():
    return tornado.web.Application(
        [(r'/', MainHandler),
         (r'/userData', UserDataHandler),
         (r'/uploadImage', UploadImageHandler)],
        debug=False,
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    server = tornado.httpserver.HTTPServer(create_app())
    server.listen(port)
    tornado.ioloop.IOLoop.current().start()
