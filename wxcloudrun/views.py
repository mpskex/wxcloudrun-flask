from datetime import datetime
from flask import render_template, request, jsonify
from run import app
import os
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
from requests import get
from os import environ

# TOKEN = os.getenv("WECHAT_TOKEN", "123456")
# AES_KEY = os.getenv("WECHAT_AES_KEY", "")
# APPID = os.getenv("WECHAT_APPID", "")

SITE_NAME = environ['BACKEND']

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
        echo_str = request.args.get("echostr", "")
        return echo_str
    snd_msg = parse_message(request.data)
    print('snd_msg:\t', snd_msg)
    # resp = get(f'http://{SITE_NAME}/api/stable/{snd_msg.source}/{snd_msg.content}').content
    resp = "You said: " + snd_msg.content
    print('resp:\t', resp)
    reply = create_reply(resp, snd_msg)
    return reply.render()


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
