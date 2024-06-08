import os
import time
import json
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
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlretrieve

max_workers = 5
num_processes = 1
conn = get_connection()
MODEL = ClipModel()

download_path = os.path.join(os.path.dirname(__file__), './download_img')


def do_search_api(conn, file_path, model=MODEL, topk=10):
    data = searchSim(conn, file_path, model, topk)
    data = json.dumps(data, ensure_ascii=False)
    return data


class ApiHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers)

    @tornado.gen.coroutine
    def get(self):

        url = self.get_query_argument('url', '')  # 如果没有参数时，返回空字符串
        topk = self.get_query_argument('topk', '10')
        topk = int(topk)
        time1 = time.time()
        print(f'time1:{time1}')
        ret = yield self.getSim(url, topk)
        self.write(ret)
        self.set_header('Access-Control-Allow-Origin', '*')

    @run_on_executor
    def getSim(self, url, topk):
        print(f'url:{url}')
        current_timestamp = str(arrow.utcnow().timestamp())
        current_timestamp = current_timestamp.replace('.', '')
        filename = re.search(r'([-_\w]+\.(?:jpg|jpeg|png))', url, re.I).group(1)
        filename = current_timestamp + "-" + filename
        file_path = os.path.join(download_path, filename)
        print(f'file_path:{file_path}')
        urlretrieve(url, file_path)
        ret = do_search_api(conn, file_path, MODEL, topk)
        return ret


def model_server():
    addr = "127.0.0.1"
    port = 8084
    print("bind: %s" % addr)
    app = tornado.web.Application(handlers, debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    http_server.start(num_processes=num_processes)
    tornado.ioloop.IOLoop.instance().start()


handlers = [
    (r"/file", ApiHandler),
]


if __name__ == '__main__':
    model_server()
