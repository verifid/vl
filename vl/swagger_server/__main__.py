#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from swagger_server import app

def main():
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Identity Verification Layer'})
    app.run(port=8080)

if __name__ == '__main__':
    main()
