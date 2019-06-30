import os
import connexion
import six
import uuid
import asyncio
import json

import vl.util

from flask import jsonify
from vl.models.user import User
from vl.models.api_response import ApiResponse
from vl.models.user_data_response import UserDataResponse
from vl.models.user_id import UserId
from vl import store
from facereg import google_images
from mocr import TextRecognizer

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
            response = jsonify({'code': 400, 'type': 'error',
                    'message': 'Request has missing values.'})
            response.status_code = 400
            return response
        else:
            u_id = user_id()
            loop.run_until_complete(download_images(json_body['name'], json_body['surname'], u_id))
            store.keep(u_id, json.dumps(json_body))
            response = jsonify({'code': 200, 'type': 'success', 
                    'message': 'User created with received values.',
                    'userId': u_id})
            response.status_code = 200
            return response
    else:
        response = jsonify({'code': 400, 'type': 'error',
                'message': 'Request needs a user json object.'})
        response.status_code = 400
        return response

def get_texts(user_id):
    image_path = os.getcwd() + '/testsets/' + 'identity' + '/' + user_id + '/' + 'image.png'
    east_path = os.getcwd() + '/vl' + '/' + 'model/frozen_east_text_detection.pb'
    text_recognizer = TextRecognizer(image_path, east_path)
    (image, _, _) = text_recognizer.load_image()
    (resized_image, ratio_height, ratio_width, _, _) = text_recognizer.resize_image(image, 320, 320)
    (scores, geometry) = text_recognizer.geometry_score(east_path, resized_image)
    boxes = text_recognizer.boxes(scores, geometry)
    results = text_recognizer.get_results(boxes, image, ratio_height, ratio_width)
    if results:
        texts = ''
        for text_bounding_box in results:
            text = text_bounding_box[1]
            texts += text + ' '
        return texts
    return ''

def verify(body):
    """Verifies user.

    :param body: User id that required for verification.
    :type body: dict | bytes

    :rtype: UserVerificationResponse
    """

    if connexion.request.is_json:
        body = UserId.from_dict(connexion.request.get_json())
        user_id = body.user_id
        user = store.value_of(user_id)
        if user == None:
            response = jsonify({'code': 400, 'type': 'error',
                'message': 'Invalid user id.'})
            response.status_code = 400
            return response
        texts = get_texts(user_id)
        print(texts)
        response = jsonify({'code': 200, 'type': 'success',
                                'message': 'Given user has verified!'})
        response.status_code = 200
        return response
