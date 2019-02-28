import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


def user_data(body):  # noqa: E501
    """Creates a user for verification.

     # noqa: E501

    :param body: User object that needs to be added temporarly
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
