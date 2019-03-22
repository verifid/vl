import os
import connexion
import six
import json

import vl.util
from vl.models.api_response import ApiResponse
from vl import store

def save_image(user_id, file, identity):
    if identity:
        path = 'identity/'
    else:
        path = 'profile/'
    directory = os.getcwd() + '/testsets/' + path +  user_id + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = directory + file.filename
    file.save(file_path, buffer_size=16384)
    file.close()

def upload_identity(userId, file):
    """Uploads an identity card image.

    :param userId: ID of user to update.
    :type userId: str
    :param file: Identity picture to upload.
    :type file: werkzeug.datastructures.FileStorage

    :rtype: ApiResponse
    """

    if store.value_of(userId) is None:
        return {'code': 204, 'type': 'error',
                'message': 'No user found with given user id.'}
    save_image(userId, file, identity=True)
    return {'code': 200, 'type': 'success',
            'message': 'Image file received.'}

def upload_profile(userId, file):
    """Uploads a profile image.

    :param userId: ID of user to update.
    :type userId: str
    :param file: Profile picture to upload.
    :type file: werkzeug.datastructures.FileStorage

    :rtype: ApiResponse
    """

    if store.value_of(userId) is None:
        return {'code': 204, 'type': 'error',
                'message': 'No user found with given user id.'}
    save_image(userId, file, identity=False)
    return {'code': 200, 'type': 'success',
            'message': 'Image file received.'}
