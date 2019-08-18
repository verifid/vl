#!/usr/bin/env python3

import os
import connexion

from vl.encoder import JSONEncoder
from crontab import CronTab
from flask_cors import CORS

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = JSONEncoder
CORS(app.app)
app.add_api('swagger.yaml', arguments={'title': 'Identity Verification Layer'})
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)

cron = CronTab(user=True)
cron_job = cron.new(command='python vl/delete_directory.py', comment='Delete test folder every night.')
cron_job.minute.on(0)
cron_job.hour.on(0)
cron_job.enable()
cron.write()
cron_job_standard_output = cron_job.run()
print(cron_job_standard_output)
