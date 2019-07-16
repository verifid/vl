import os

from flask import jsonify
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
    _, file_extension = os.path.splitext(file.filename)
    file_path = directory + 'image' + file_extension
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
        response = jsonify({'code': 204, 'type': 'error',
                'message': 'No user found with given user id.'})
        response.status_code = 204
        return response
    save_image(userId, file, identity=True)
    response = jsonify({'code': 200, 'type': 'success',
            'message': 'Image file received.'})
    response.status_code = 200
    return response

def upload_profile(userId, file):
    """Uploads a profile image.

    :param userId: ID of user to update.
    :type userId: str
    :param file: Profile picture to upload.
    :type file: werkzeug.datastructures.FileStorage

    :rtype: ApiResponse
    """

    if store.value_of(userId) is None:
        response = jsonify({'code': 204, 'type': 'error',
                'message': 'No user found with given user id.'})
        response.status_code = 204
        return response
    save_image(userId, file, identity=False)
    response = jsonify({'code': 200, 'type': 'success',
            'message': 'Image file received.'})
    response.status_code = 200
    return response
