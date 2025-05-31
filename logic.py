import json
import time
import io, base64
from PIL import Image
import datetime
from config import YOUR_KEY, YOUR_SECRET


import requests


class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "style": 'PIXEL_ART',
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f'{prompt}'
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)


def generate_image(path, text):
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', YOUR_KEY, YOUR_SECRET)
    pipeline_id = api.get_pipeline()
    uuid = api.generate(text, pipeline_id,images=1)
    t1 = datetime.datetime.now()
    files = api.check_generation(uuid)
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(files[0], "utf-8"))))
    img.save(path)
    t2 = datetime.datetime.now()
    print(t2 - t1)
