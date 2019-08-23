import os
import connexion
import uuid
import asyncio
import json
import cv2
import requests
import base64

from vl.models.api_response import ApiResponse  # noqa: E501
from vl.models.error import Error  # noqa: E501
from vl.models.user import User  # noqa: E501
from vl.models.user_data_response import UserDataResponse  # noqa: E501
from vl.models.user_id import UserId  # noqa: E501
from vl.models.user_verification_response import UserVerificationResponse  # noqa: E501
from vl import util

from re import search
from flask import jsonify
from flask import request
from vl.models.verify_user import VerifyUser
from vl.models.user import User
from vl.models.image_upload import ImageUpload
from vl import store
from facereg import google_images
from facereg import face_encoder
from facereg import recognize_faces
from mocr import TextRecognizer
from mocr import face_detection
from nerd import ner

def save_image(user_id, image_str, identity):
    if identity:
        path = 'identity/'
    else:
        path = 'profile/'
    directory = os.getcwd() + '/testsets/' + path +  user_id + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = directory + 'image' + '.jpg'
    image_data = base64.b64decode(image_str)
    with open(file_path, 'wb') as f:
        f.write(image_data)

    # detect face from identity image
    if identity:
        face_image = face_detection.detect_face(file_path)
        face_directory = os.getcwd() + '/testsets/' + 'face/' + user_id + '/'
        if not os.path.exists(face_directory):
            os.makedirs(face_directory)
        cv2.imwrite(face_directory + 'image.jpg', face_image)

loop = asyncio.get_event_loop()

json_model = ['country', 'dateOfBirth', 'name', 'surname']
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


def send_user_data(body):  # noqa: E501
    """send_user_data

    Creates a new user for verification. Duplicates are allowed. # noqa: E501

    :param body: User going to be verified.
    :type body: dict | bytes

    :rtype: UserDataResponse
    """
    if connexion.request.is_json:
        json_body = connexion.request.get_json()
        if validate_json(json_body) == False:
            error = Error(code=400, message='Request has missing values.')
            return error, 400
        else:
            u_id = user_id()
            store.keep(u_id, json.dumps(json_body))
            response = UserDataResponse(code=200, type='success',
                                        message='User created with received values.', user_id=u_id)
            return response, 200
    else:
        error = Error(code=400, message='Request needs a user json object.')
        return error, 400


def upload_identity():  # noqa: E501
    """upload_identity

    Uploads an identity image. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponse
    """
    if connexion.request.is_json:
        body = ImageUpload.from_dict(connexion.request.get_json())  # noqa: E501
        user_id = body.user_id
        identity_image = body.image
        if user_id is None or identity_image is None:
            error = Error(code=400, message='User id or image parameter is not given.')
            return error, 400
        if store.value_of(user_id) is None:
            response = ApiResponse(code=204, type='error', message='No user found with given user id.')
            return response, 204
        save_image(user_id, identity_image, identity=True)
        response = ApiResponse(code=200, type='success', message='Identity image file received.')
        return response, 200
    else:
        error = Error(code=400, message='Provide a json payload that contains userId and image data string.')
        return error, 400


def upload_profile(body=None):  # noqa: E501
    """upload_profile

    Uploads a profile image. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponse
    """
    if connexion.request.is_json:
        body = ImageUpload.from_dict(connexion.request.get_json())  # noqa: E501
        user_id = body.user_id
        profile_image = body.image
        if user_id is None or profile_image is None:
            error = Error(code=400, message='User id or image parameter is not given.')
            return error, 400
        if store.value_of(user_id) is None:
            response = ApiResponse(code=204, type='error', message='No user found with given user id.')
            return response, 204
        save_image(user_id, profile_image, identity=False)
        response = ApiResponse(code=200, type='success', message='Profile image file received.')
        return response, 200
    else:
        error = Error(code=400, message='Provide a json payload that contains userId and image data string.')
        return error, 400


def get_texts(user_id):
    image_path = os.getcwd() + '/testsets/' + 'identity' + '/' + user_id + '/' + 'image.jpg'
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

def recognize_face(user_id):
    datasets_path = os.getcwd() + '/testsets/identity/' + user_id
    encodings_path = os.path.dirname(os.path.realpath(__file__)) + '/encodings.pickle'
    face_encoder.encode_faces(datasets=datasets_path, encodings=encodings_path, detection_method='cnn')
    image_path = os.getcwd() + '/testsets/face/' + user_id + '/' + 'image.jpg'
    names = recognize_faces.recognize(image_path, datasets=datasets_path, encodings=encodings_path, detection_method='cnn')
    return names

def point_on_recognition(names, user_id):
    point = 0
    if not names:
        point = 0
    if len(names) > 1:
        for name in names:
            if name == user_id:
                point = 25
    else:
        if names[0] == user_id:
            point = 25
    return point

def verify(body):  # noqa: E501
    """verify

    Verifies user with given user id. # noqa: E501

    :param body: User id that is required for verification.
    :type body: dict | bytes

    :rtype: UserVerificationResponse
    """
    if connexion.request.is_json:
        body = VerifyUser.from_dict(connexion.request.get_json())  # noqa: E501
        user_id = body.user_id
        user_json = store.value_of(user_id)
        if user_json == None:
            response = Error(code=400, message='Invalid user id.')
            return response, 400
        user_dict = json.loads(user_json)
        user = User.from_dict(user_dict)
        texts = get_texts(user_id)
        if not texts:
            response = Error(code=400, message='Can not recognize characters from identity card.')
            return response, 400
        language = body.language
        doc_text_label = get_doc(texts, language=language)
        user_text_label = create_user_text_label(user)
        text_validation_point = validate_text_label(doc_text_label, user_text_label)
        print('text_validation_point: ' + str(text_validation_point))
        names = recognize_face(user_id)
        if not names:
            response = Error(code=400, message='Can not recognize face from identity card.')
            return response, 400
        face_validation_point = point_on_recognition(names, user_id)
        print('face_validation_point: ' + str(face_validation_point))
        verification_rate = text_validation_point + face_validation_point
        response = UserVerificationResponse(code=200, verification_rate=verification_rate)
        return response, 200
    else:
        error = Error(code=400, message='Provide a json payload that contains userId')
        return error, 400
