# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time

from datetime import timedelta

# 设置允许的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        lst = []
        n = 10
        cnt = 0
        for i in os.listdir('static/images/'):
            url = 'static/images/' + i
            dic = {"url": url}
            lst.append(dic)
            cnt += 1
            if cnt == n:
                break

        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径

        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        # img = cv2.imread(upload_path)
        # cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)

        return render_template('display.html', inputs=lst, num=n, val1=time.time())

    return render_template('upload.html')


@app.route('/get', methods=['GET'])
def get_param():
    dic = {}
    param = {
        "name": "james",
        "age": 35,
        "height": 183,
        "nums": 15,
        "id": 0x1545ED
    }
    dic["param"] = param

    return dic


@app.route('/image')
def get_images():
    lst = []
    dic = {}
    n = 10
    cnt = 0
    for i in os.listdir('static/images/'):
        url = 'static/images/' + i
        dic = {"url": url}
        lst.append(dic)
        cnt += 1
        if cnt == n:
            break
    dic["param"] = lst
    return dic


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25000, debug=True)
