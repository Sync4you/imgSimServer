# encoding: utf-8
# @Author: William·Woo
# @Time:2024-01-14-5:07 PM
# @File:press_test.py


from locust import HttpUser, task, tag, between, SequentialTaskSet
import random


class ImgSearchTaskCase(SequentialTaskSet):
    def __init__(self):
        super()
        self.id = int(random.random() * 1000)

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def say(self):
        print(self.id)


class WebUser(HttpUser):
    tasks = [ImgSearchTaskCase]
    min_wait = 1000
    max_wait = 1000

