# coding:utf-8
import json
from flask import Flask, render_template, request
from flask_cors import CORS
import os
import requests
from model.Model import ClipModel
from milvus.SearchImage import searchSim, get_connection
from gevent import monkey
from datetime import timedelta


# 设置允许的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG'}

# global MODEL
# global conn
monkey.patch_all()
conn = get_connection()
MODEL = ClipModel()

app = Flask(__name__)
# 设置静态文件缓存过期时间
CORS(app)
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/file', methods=['POST', 'GET'])
def url_search():
    if request.method == 'GET':
        url = request.args.get('url')
        topk = request.args.get('topk')
        topk = int(topk)
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        file_path = os.path.join(basepath, 'static/cached_images', 'test.jpg')
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            open(file_path, 'wb').write(res.content)
            data = searchSim(conn, file_path, MODEL, topk)
            data = json.dumps(data, ensure_ascii=False)
            return data, 200


if __name__ == '__main__':
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('127.0.0.1', 8085), app)
    server.serve_forever()
