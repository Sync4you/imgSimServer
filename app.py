# coding:utf-8
import json
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, send_file, \
    send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import cv2
import time
import requests
from model.Model import ClipModel
from milvus.SearchImage import searchSim, get_connection

from datetime import timedelta


# 设置允许的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG'}

# global MODEL
# global conn

conn = get_connection()
MODEL = ClipModel()

app = Flask(__name__)
# 设置静态文件缓存过期时间
CORS(app)
app.send_file_max_age_default = timedelta(seconds=1)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# @app.route('/url_upload', methods=['POST'])
# def url_upload():
#     if request.method == 'POST':
#
#         # url = request.form.get('url_input')
#         url = request.args.get('url')
#         topk = request.args.get('topk')
#         if topk is None:
#             topk = 10
#         topk = int(topk)
#         basepath = os.path.dirname(__file__)  # 当前文件所在路径
#         url_path = basepath + "/static/url_images"
#         if os.path.exists(url_path) is False:
#             os.mkdir(url_path)
#         res = requests.get(url, stream=True)
#         if res.status_code == 200:
#             img_path = url_path + "/tmp.jpg"
#             open(img_path, 'wb').write(res.content)
#             res = searchSim(conn, img_path, MODEL, topk=topk)
#
#             res = json.dumps(res, ensure_ascii=False)
#             return res
#         else:
#             return "failed"
#     else:
#         return "get"
#
#
@app.route('/upload', methods=['POST'])  # 添加路由
def upload():
    if request.method == 'POST':

        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        user_input = request.form.get("name")
        topk = request.form.get('topk')
        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        output_path = basepath + '/static/output_images/'
        if os.path.exists(output_path):
            os.system(f"rm -rf {output_path}")
        os.mkdir(output_path)

        if os.path.exists(basepath + '/static/cached_images'):
            path = basepath + '/static/cached_images'
            os.system(f"rm -rf {path}")

        os.mkdir(basepath + '/static/cached_images')

        cached_path = os.path.join(basepath, 'static/cached_images', 'test.jpg')  # 缓存文件路径

        if os.path.exists(basepath + '/static/uploaded_images') is False:
            os.mkdir(basepath + '/static/uploaded_images')
        upload_path = os.path.join(basepath, 'static/uploaded_images', secure_filename(f.filename))

        f.save(upload_path)

        img = cv2.imread(upload_path)
        cv2.imwrite(cached_path, img)

        res = searchSim(conn, cached_path, MODEL, topk)
        data_list = res["output"]
        cnt = 0
        for dic in data_list:
            _id = dic["id"]
            _dist = dic["distance"]
            _path = dic["path"]
            # os.system(f"cp {_path} {output_path}{cnt}.jpg")
            cnt += 1

        res = json.dumps(res, ensure_ascii=False)
        return render_template('display.html', data=res)


@app.route('/url_search', methods=['POST', 'GET'])
def url_search():
    if request.method == 'POST':
        url = request.form.get('url_input')
        topk = request.form.get('topk')
        if topk is None:
            topk = 10
        else:
            topk = int(topk)

        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        file_path = os.path.join(basepath, 'static/cached_images', 'test.jpg')
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            open(file_path, 'wb').write(res.content)
            data = searchSim(conn, file_path, MODEL, topk)
            data = json.dumps(data, ensure_ascii=False)
            return render_template('display.html', data=data)
        else:
            return "failed", 405
    else:
        return render_template('upload.html')
        # url = request.args.get('url')
        # topk = request.args.get('topk')
        # topk = int(topk)
        # basepath = os.path.dirname(__file__)  # 当前文件所在路径
        # file_path = os.path.join(basepath, 'static/cached_images', 'test.jpg')
        # res = requests.get(url, stream=True)
        # if res.status_code == 200:
        #     open(file_path, 'wb').write(res.content)
        #     data = searchSim(conn, file_path, MODEL, topk)
        #     data = json.dumps(data, ensure_ascii=False)
        #     return data, 200


def return_img_stream(img_local_path):
    """
  工具函数:
  获取本地图片流
  :param img_local_path:文件单张图片的本地绝对路径
  :return: 图片流
  """
    import base64
    img_stream = ''
    with open(img_local_path, 'r') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream

#
# @app.route('/<image_name>', methods=['GET'])
# def image_path(image_name):
#     if os.path.exists('/' + image_name):
#         return return_img_stream('/' + image_name)
#     return image_name
#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25002, debug=True)
