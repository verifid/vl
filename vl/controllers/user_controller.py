import os
import connexion
import uuid
import asyncio
import json

from re import search
from flask import jsonify
from vl.models.user_id import UserId
from vl.models.user import User
from vl import store
from facereg import google_images
from mocr import TextRecognizer
from nerd import ner

loop = asyncio.get_event_loop()

json_model = ['country', 'dateOfBirth', 'gender', 
            'name', 'placeOfBirth', 'surname']
entity_tags = {'PERSON': 'name', 'DATE': 'date', 'GPE': 'nationality', 'NORP': 'city'}

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

def get_doc(texts, language):
    doc = ner.name(texts, language=language)
    text_label = [(X.text, X.label_) for X in doc]
    return text_label

def create_user_text_label(user):
    user_text_label = {'PERSON': [user.name, user.surname],
                       'DATE': user.date_of_birth,
                       'GPE': user.country}
    return user_text_label

def point_on_texts(text, value):
    val_len = len(value)
    text_len = len(text)
    if text_len > val_len:
        match = search(value, text)
    else:
        match = search(text, value)
    point = 0
    if match:
        (start, end) = match.span()
        point = int(((100 * (end - start)) / val_len) / 4)
    return point

def validate_text_label(text_label, user_text_label):
    result = 0
    for (text, label) in text_label:
        if label in user_text_label:
            value = user_text_label[label]
            # check for name and surname
            if isinstance(value, list):
                for val in value:
                    result += point_on_texts(text, val)
            else:
                result += point_on_texts(text, value)
    return result

def verify(body):
    """Verifies user.

    :param body: User id and language that required for verification.
    :type body: dict | bytes

    :rtype: UserVerificationResponse
    """

    if connexion.request.is_json:
        body = UserId.from_dict(connexion.request.get_json())
        user_id = body.user_id
        user_json = store.value_of(user_id)
        if user_json == None:
            response = jsonify({'code': 400, 'type': 'error',
                'message': 'Invalid user id.'})
            response.status_code = 400
            return response
        user_dict = json.loads(user_json)
        user = User.from_dict(user_dict)
        texts = get_texts(user_id)
        if not texts:
            response = jsonify({'code': 400, 'type': 'error',
                                'message': 'Can not recognize characters from identity card.'})
            response.status_code = 400
            return response
        language = body.language
        doc_text_label = get_doc(texts, language=language)
        user_text_label = create_user_text_label(user)
        text_validation_point = validate_text_label(doc_text_label, user_text_label)
        print(text_validation_point)
        response = jsonify({'code': 200, 'type': 'success',
                                'message': 'Given user has verified!'})
        response.status_code = 200
        return response
