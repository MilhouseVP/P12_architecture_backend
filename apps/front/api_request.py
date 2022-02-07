import os
import requests


def api_login():
    url = 'http://127.0.0.1:8000/api/login/'
    data = {
        'username': 'support1@test.test',
        'password': 'totototo1'
    }

    req = requests.post(url, data=data)
    return req.json()
