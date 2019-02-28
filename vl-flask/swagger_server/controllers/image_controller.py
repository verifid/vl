import connexion
import six

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server import util


def upload_file(userId, file):  # noqa: E501
    """Uploads an image

     # noqa: E501

    :param userId: ID of user to update
    :type userId: str
    :param file: file to upload
    :type file: werkzeug.datastructures.FileStorage

    :rtype: ApiResponse
    """
    return 'do some magic!'
