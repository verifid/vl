import os
import connexion
import six
import uuid
import asyncio
import json

import vl.util

from vl.store.redis_store import RedisStore
from vl.models.user import User
from vl.models.api_response import ApiResponse
from vl.models.user_data_response import UserDataResponse
from redis import Redis
from facereg import google_images

redis = Redis(host='localhost', port=6379)
store = RedisStore(redis)
loop = asyncio.get_event_loop()

json_model = ['country', 'dateOfBirth', 'gender', 
            'name', 'placeOfBirth', 'surname']

def validate_json(json_object):
    if set(json_object.keys()) != set(json_model):
        return False
    for key in json_model:
        if json_object[key] == None:
            return False
    return True

def user_id():
    return str(uuid.uuid4())

async def download_images(name, surname, user_id):
    output_directory = os.getcwd() + '/datasets/' + user_id
    _, _ = google_images.download(str.format('{0} {1}', name, surname),
                            limit=3, output_directory=output_directory)

def send_data(body):
    """Creates a user for verification.

    :param body: User object that needs to be added temporarly.
    :type body: dict | bytes

    :rtype: None
    """

    if connexion.request.is_json:
        json_body = connexion.request.get_json()
        if validate_json(json_body) == False:
            response = ApiResponse.from_dict({'code': 400, 'type': 'error',
                                        'message': 'Request has missing values.'})
            return response.to_str()
        else:
            u_id = user_id()
            loop.run_until_complete(download_images(json_body['name'], json_body['surname'], u_id))
            store.keep(u_id, json.dumps(json_body))
            response = UserDataResponse.from_dict({'code': 200, 'type': 'success', 
                                        'message': 'User created with received values.',
                                        'userId': u_id})
            return response.to_str()
    else:
        response = ApiResponse.from_dict({'code': 400, 'type': 'error',
                                        'message': 'Request needs a user json object.'})
        return response.to_str()
