import os
from flask import Flask, send_file
from flask_cors import CORS


app = Flask(__name__)
# 设置静态文件缓存过期时间
CORS(app)
base_path = "../../../mnt/weeddata/imgs/"


@app.route('/<image_class>/<sub>/<image_path>', methods=['GET'])
def get_image(image_class, sub, image_path):
    import base64
    img_stream = ''
    path = base_path + image_class + '/' + sub + '/' + image_path
    if os.path.exists(path):
        return send_file(path), 200
    else:
        return "File not exist", 405
    # with open(base_path + image_class + '/' + sub + '/' + image_path, 'rb') as img_f:
    #     img_stream = img_f.read()
    #     img_stream = base64.b64encode(img_stream)
    # return img_stream.decode(encoding="utf-8")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=25001, debug=True)
