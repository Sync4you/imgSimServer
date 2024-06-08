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

download_path = os.path.join(os.path.dirname(__file__), './download_img')


class ApiHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.model = ClipModel()
        self.conn = get_connection()

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
        print("write image done")
        ret = await self.do_search_api(self.conn, file_path, self.model, topk)
        print("search done")
        # get the feats vector
        # self.write(json.dumps(ret))

        self.write(ret)
        self.set_header('Access-Control-Allow-Origin', '*')
        print("return the result")

    async def getSim(self, url):
        print(f'url:{url}')
        # urlretrieve(url, file_path)
        response = ""
        try:
            response = await tornado.httpclient.AsyncHTTPClient().fetch(url)

        except Exception as e:
            print("Error: %s" % e)

        return response.body

    async def do_search_api(self, conn, file_path, model, topk=10):
        data = searchSim(conn, file_path, model, topk)
        print("search done")
        data = json.dumps(data, ensure_ascii=False)
        return data



handlers = [
    (r"/file", ApiHandler),
]


if __name__ == '__main__':
    app = tornado.web.Application(handlers, debug=True)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8085)
    server.start(2)
    tornado.ioloop.IOLoop.instance().start()

