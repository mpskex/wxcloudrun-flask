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

# TOKEN = os.getenv("WECHAT_TOKEN", "123456")
# AES_KEY = os.getenv("WECHAT_AES_KEY", "")
# APPID = os.getenv("WECHAT_APPID", "")

SITE_NAME = getenv('BACKEND', '')
API_KEY = getenv('MQ_API_KEY', 'wechat')
API_SECRET = getenv('MQ_API_SECRET', '')

auth = url_safe.URLSafeTimedSerializer(API_SECRET, API_KEY)

@app.route('/api/chat', methods=['POST', 'GET'])
def send():
    # signature = request.args.get("signature", "")
    # timestamp = request.args.get("timestamp", "")
    # nonce = request.args.get("nonce", "")
    # encrypt_type = request.args.get("encrypt_type", "raw")
    # msg_signature = request.args.get("msg_signature", "")
    # try:
    #     check_signature(TOKEN, signature, timestamp, nonce)
    # except InvalidSignatureException:
    #     abort(403)
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
        resp = requests.get(f'http://{SITE_NAME}/api/{API_KEY}/{auth.dumps(s)}').content
        resp = json.loads(resp)['message']
    except Exception as e:
        resp = "API 失败: \n" + traceback.format_exc() + '\n\n' + str(resp) + '\n\n' + str(s)
    print('resp:\t', resp)
    reply = create_reply(resp, snd_msg)
    return reply.render()


