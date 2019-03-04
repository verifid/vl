import os
import connexion
import six

import vl.util
from vl.models.api_response import ApiResponse
from vl.store.redis_store import RedisStore
from redis import Redis
from enum import Enum

redis = Redis(host='localhost', port=6379)
store = RedisStore(redis)

def save_image(user_id, file):
     directory = os.getcwd() + '/testsets/' + user_id + '/'
     if not os.path.exists(directory):
        os.makedirs(directory)
     file_path = directory + file.filename
     file.save(file_path, buffer_size=16384)
     file.close()

def upload_image(userId, file):
    """Uploads an image.

    :param userId: ID of user to update.
    :type userId: str
    :param file: Image file to upload.
    :type file: werkzeug.datastructures.FileStorage

    :rtype: ApiResponse
    """

    if not userId:
        api_response = ApiResponse.from_dict({'code': 400, 'type': 'error',
                                        'message': 'No user id found on request.'})
        return api_response.to_str()
    if not file:
        api_response = ApiResponse.from_dict({'code': 412, 'type': 'error',
                                        'message': 'No file found on request.'})
        return api_response.to_str()
    save_image(userId, file)
    api_response = ApiResponse.from_dict({'code': 200, 'type': 'success',
                                        'message': 'Image file received.'})
    return api_response.to_str()
