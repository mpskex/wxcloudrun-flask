from datetime import datetime
from flask import request
import json
from run import app
import traceback

from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
from itsdangerous import url_safe
import requests
from os import getenv

SITE_NAME = getenv('BACKEND', '')
API_KEY = getenv('MQ_API_KEY', 'wechat')
API_SECRET = getenv('MQ_API_SECRET', '')

auth = url_safe.URLSafeTimedSerializer(API_SECRET, API_KEY)

@app.route('/api/chat', methods=['POST', 'GET'])
def send():
    if request.method == "GET":
        return ""
    try:
        snd_msg = parse_message(request.data)
    except KeyError:
        return ""
    s = json.dumps({
        'user_id': snd_msg.source,
        'type': 'text',
        'content': snd_msg.content
    })
    try:
        resp = requests.get(f'http://{SITE_NAME}/api/{API_KEY}/{auth.dumps(s)}', headers={'host': 'baidu.com'}).content
        resp = json.loads(resp)['message']
    except Exception as e:
        resp = "API 失败: \n" + traceback.format_exc() + '\n\n' + str(type(resp)) + resp.decode('utf-8') + '\n\n' + str(s)
    print('resp:\t', '!' + resp)
    reply = create_reply(resp, snd_msg)
    return reply.render()


