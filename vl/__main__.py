#!/usr/bin/env python3

import connexion

from vl.encoder import JSONEncoder

app = connexion.App(__name__, specification_dir='./swagger/')

def main():
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Identity Verification Layer'})
    app.run(port=5000)

if __name__ == '__main__':
    main()
