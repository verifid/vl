#!/usr/bin/env python3

import connexion

from vl.encoder import JSONEncoder

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'Identity Verification Layer'})
app.run(host='0.0.0.0', port=8080)
