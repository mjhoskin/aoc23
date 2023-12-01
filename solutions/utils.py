import json
import os

import requests

def neo4j_config_local(password:str, port:int=7474) -> dict:
    return {
        "url": f'http://localhost:{port}/db/neo4j/tx/commit',
        "headers": {
            'Accept': 'application/json; charset=UTF-8',
            'Authorization': f'Basic {password}',
            'Content-Type':'application/json'
        }
    }

def get_path(day, test: bool = False):
  ext = '.txt'
  if test:
    ext += '.test'
  path = os.path.join(os.getcwd(), 'data', f'day{day}{ext}')
  
  return path

def post(config, data):
  return requests.post(
    config['url'],
    headers=config['headers'],
    data = json.dumps(data)
  )
