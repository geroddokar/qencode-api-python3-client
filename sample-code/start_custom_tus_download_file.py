#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qencode3
import time
import json
from qencode3 import QencodeClientException, QencodeTaskException, upload


API_KEY = 'your-api-qencode-key'
file_path = 'your-path-to-file'

params = qencode3.custom_params()

FORMAT = qencode3.format()

FORMAT.size = "320x240"
FORMAT.output = "mp4"

params.source = ''
params.format = [FORMAT]


def start_encode():
 
  clientq = qencode3.client(API_KEY)
  if clientq.error:
    raise QencodeClientException(clientq.message)

  print('The client created. Expire date: %s' % clientq.expire)
  task = clientq.create_task()
  if task.error:
    raise QencodeTaskException(task.message)

  fileUrl = task.upload_url +'/'+ task.task_token

  res = upload(file_path=file_path,url=fileUrl, log_func=log_upload, chunk_size=200000)
  params.source = res.url
  task.custom_start(params)
  if task.error:
    raise QencodeTaskException(task.message)

  print('Start encode. Task: %s' % task.task_token)

  while True:
    status = task.status()
    # print status
    print(json.dumps(status, indent=2, sort_keys=True))
    if status['error'] or status['status'] == 'completed':
      break
    time.sleep(5)

def log_upload(msg):
  print(msg)


if __name__ == '__main__':
  start_encode()