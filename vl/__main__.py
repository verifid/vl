#!/usr/bin/env python3

import connexion

from vl import encoder
from flask_cors import CORS

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    CORS(app.app)
    app.add_api('swagger.yaml', arguments={'title': 'Identity Verification Layer'}, pythonic_params=True)
    app.run(port=8080)


if __name__ == '__main__':
    main()
