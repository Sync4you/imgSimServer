import os
import time
import json
import argparse
import re
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.web
import tornado.gen
import arrow

from model.Model import ClipModel
from milvus.SearchImage import searchSim, get_connection


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.web
import tornado.gen


conn = None
MODEL = None


def load_conn():
    global conn
    conn = get_connection()


def load_model():
    global MODEL
    MODEL = ClipModel()


download_path = os.path.join(os.path.dirname(__file__), './download_img')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o','--operation',
        default=4,
        type=int,
        help='type of operations,1 for train,2 for train continue,3 for predict.')
    parser.add_argument(
        '--server',
        type=str,
        default='127.0.0.1',
        help='server')
    return parser.parse_known_args()


def do_search_api(conn, file_path, model=MODEL, topk=10):
    data = searchSim(conn, file_path, model, topk)
    data = json.dumps(data, ensure_ascii=False)
    return data


class ApiHandler(tornado.web.RequestHandler):
    async def get(self):
        current_timestamp = str(arrow.utcnow().timestamp())
        current_timestamp = current_timestamp.replace('.', '')
        url = self.get_query_argument('url', '')  # 如果没有参数时，返回空字符串
        topk = self.get_query_argument('topk', '10')
        topk = int(topk)
        time1 = time.time()
        print(f'time1:{time1}')
        ret = await self.getSim(url)
        filename = re.search(r'([-_\w]+\.(?:jpg|jpeg|png))', url, re.I).group(1)
        filename = current_timestamp + "-" + filename
        file_path = os.path.join(download_path, filename)
        print(f'file_path:{file_path}')

        with open(file_path, "wb") as f:
            f.write(ret)
        ret = do_search_api(conn, file_path, MODEL, topk)

        # get the feats vector
        # self.write(json.dumps(ret))

        self.write(ret)
        self.set_header('Access-Control-Allow-Origin', '*')

    async def getSim(self, url):
        print(f'url:{url}')
        # urlretrieve(url, file_path)
        response = ""
        try:
            response = await tornado.httpclient.AsyncHTTPClient().fetch(url)
        except Exception as e:
            print("Error: %s" % e)

        return response.body


def model_server():
    addr = "127.0.0.1"
    port = 8083
    print("bind: %s" % addr)
    app = tornado.web.Application(handlers, debug=True)
    http_server = tornado.httpserver.HTTPServer(app)

    # sockets = tornado.netutil.bind_sockets(port)
    # tornado.process.fork_processes(10)
    # http_server.add_sockets(sockets)

    http_server.listen(port)
    http_server.start(num_processes=1)   # 根据CPU核数fork工作进程个数
    tornado.ioloop.IOLoop.instance().start()


handlers = [
    (r"/file", ApiHandler),
]


if __name__ == '__main__':
    load_conn()
    load_model()
    model_server()
