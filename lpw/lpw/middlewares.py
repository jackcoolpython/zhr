# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
from .IP_logic import IP_logic
import threading
import time


class IPDownloaderMiddleware(object):
    def __init__(self):
        super(IPDownloaderMiddleware,self).__init__()
        #默认起始IP为空
        self.now_IP = None
        #获取IP代理网站的url（极光代理网）
        self.update_ip_url = 'http://d.jghttp.golangapi.com/getip?num=1&type=2&pro=&city=0&yys=0&port=11&pack=20585&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
        #添加请求头信息
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        #更新一个IP到now_IP
        self.update_IP()
        #启用多线程，在异步请求的情况下可能会出现拥塞的现象，该多线程的作用就是防止拥塞现象的产生
        th = threading.Thread(target=self.update_IP_in_thread)
        th.start()
        #为了线程安全，启用锁机制
        self.lock = threading.Lock()

    def process_request(self, request, spider):
        #将已经使用的IP通过meta传入response，以备后续使用
        request.mate['IPproxy'] = self.now_IP.IP_url
        return None

    def process_response(self, request, response, spider):
        #根据返回状态码来进行判定是否被黑，以后会添加返回验证码时的方案
        if response.status != 200:
            #线程上锁保证线程安全
            self.lock.acquire()
            self.now_IP.is_blacked = True
            #线程解锁让后面的请求获得线程资源
            self.lock.release()
            #如果IP被黑则需要返回request进行重新更新
            return request
        #如果IP没有问题则返回response传递给item
        return response


    #更新IP信息到now_IP
    def update_IP(self):
        resp = requests.get(self.update_ip_url,headers = self.headers)
        IP_detil = IP_logic(resp.json())
        self.now_IP = IP_detil
        print("当前IP:%s"%self.now_IP.IP_url)



    def update_IP_in_thread(self):
        #在当前线程中进行定时，每10s count增加1，到30s的时候更换IP
        count = 0
        while True:
            time.sleep(10)
            if count >=3:
                self.update_IP()
                count = 0
            else:
                count += 1







