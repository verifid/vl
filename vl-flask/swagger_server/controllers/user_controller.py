import os
import connexion
import six
import uuid
import asyncio

from swagger_server.store.redis_store import RedisStore
from swagger_server.models.user import User
from swagger_server import util
from swagger_server.models.api_response import ApiResponse
from redis import Redis
from facereg import google_images

redis = Redis(host='localhost', port=6379)
store = RedisStore(redis)

json_model = ['name', 'surname', 'gender',
            'date_of_birth', 'place_of_birth', 'country']

def validate_json(body):
    if set(body) != set(json_model):
        return False
    for key in json_model:
        if body[key] == None:
            return False
    return True

def user_id():
    return str(uuid.uuid4())

@asyncio.coroutine
def download_images(name, surname, user_id):
    output_directory = os.getcwd() + '/datasets/' + user_id
    _, _ = google_images.download(str.format('{0} {1}', name, surname),
                            limit=3, output_directory=output_directory)

def user_data(body):
    """Creates a user for verification.

    :param body: User object that needs to be added temporarly
    :type body: dict | bytes

    :rtype: None
    """

    print('REQUEST : ', connexion.request)
    if connexion.request.is_json:
        if validate_json(body) == False:
            api_response = ApiResponse(code=400, type='error', message='Request has missing values.')
            return api_response.to_str()
        else:
            body = User.from_dict(connexion.request.get_json())
            user = user_id()
            yield download_images(body.name, body.surname, uuid)
            store.keep(uuid, body)
            api_response = ApiResponse.from_dict({'code': 200, 'type': 'sucess', 
                                        'message': 'User created with received values.',
                                        'userId': user})
            return api_response.to_str()
    else:
        api_response = ApiResponse(code=400, type='error', message='Request needs a user json object.')
        return api_response.to_str()
