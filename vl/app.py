#!/usr/bin/env python3

import os
import connexion

from vl.encoder import JSONEncoder

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'Identity Verification Layer'})
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
