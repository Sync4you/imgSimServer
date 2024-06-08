# encoding: utf-8
# @Author: William·Woo
# @Time:2024-01-15-2:19 PM
# @File:interface_test.py


from locust import task, tag, HttpUser, TaskSet, between
from random import randint
import json



class ImgTask(TaskSet):
    def __init__(self, parent: "User"):
        super().__init__(parent)
        self.test_data = None

    def on_start(self):
        with open(test_data_path, "r", encoding="utf-8") as f:
            d = f.readline()
            datas = []
            while d:
                line = d.strip().split('\t')
                url = line[-1]
                dic = {"url": url, "topk": 10}
                datas.append(dic)
                d = f.readline()
            self.test_data = datas
        print("on starting!")

    @task
    def test_search(self):
        randIndex = randint(1, len(self.test_data))
        response = self.client.post("/file", data=self.test_data[randIndex], catch_response=True)
        res = json.load(response.txt)
        if "distance" in res[0].keys():
            print("success")
        else:
            print("failed")


class WebSiteUser(HttpUser):
    host = "222.186.42.181:8083"
    tasks = [ImgTask]
    wait_time = between(1, 5)


if __name__ == '__main__':
    test_data_path = "data.tsv"

    host = "http://222.186.42.181:8083/file"
    with open(test_data_path, "r", encoding="utf-8") as f:
        d = f.readline()
        datas = []
        while d:
            line = d.strip().split('\t')
            url = line[-1]
            host_url = host + "?url=" + url + "&topk=10"
            datas.append(host_url)
            print(host_url)

            d = f.readline()

