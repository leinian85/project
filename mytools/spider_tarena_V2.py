#!/usr/bin/python3

'''
    V2 : 多线程版本
'''
import requests
from fake_useragent import UserAgent
import os
from lxml import etree
import time
from threading import Thread


class TarenaSpider:
    def __init__(self, url, dir):
        self.baseurl = url
        self.auth = ("tarenacode", "code_2014")
        self.dir = dir
        self.ignore = ["../"]
        self.ua = UserAgent()
        self.new_file = []

    def get_html(self, url, is_file=False):
        headers = {"User-Agent": self.ua.random}

        if is_file:
            print("url-file:", url)
            html = requests.get(url=url, auth=self.auth, headers=headers, stream=True)
        else:
            print("url-dir:", url)
            html = requests.get(url=url, auth=self.auth, headers=headers)

        return html

    def go_next_dir(self, url, if_dir):
        if not if_dir:
            self.download(url)
            return

        html = self.get_html(url).content.decode("utf-8", "ignore")
        r_obj = etree.HTML(html)
        r_list = r_obj.xpath("//a/@href")
        for urlone in r_list:
            if urlone in self.ignore:
                continue

            dir_one = url + urlone

            # url = "http://code.tarena.com.cn/AIDCode/aid1905/14_spider/"
            # 获取上级目录 AIDCode/aid1905/14_spider/
            is_dir = False
            if dir_one.endswith("/"):
                dir = self.dir + dir_one[26:]
                is_dir = True
            else:
                dir = self.dir + "/".join(dir_one[26:].split("/")[:-2])
                is_dir = False

            if not os.path.exists(dir):
                os.makedirs(dir)

            self.go_next_dir(dir_one, is_dir)
            # time.sleep(random.randint(1, 3))

    # 下载文件
    def download(self, url):
        filename = self.dir + url[26:]
        name = url.split("/")[-1]
        if os.path.exists(filename):
            print("{} 文件已存在".format(name))
            return

        self.writh_file(filename, name, url)

    # 写入文件
    def writh_file(self, d_filename, filename, url):
        '''
        :param d_filename: 文件的下载路径
        :param filename: 文件名
        :param url: 文件下载的url
        '''
        with open(d_filename, 'wb') as f:
            with self.get_html(url=url, is_file=True) as res:
                siza_all = res.headers.get("Content-Length")
                size_sum = 0
                size_temp = 0
                starttime = time.time()
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        size_sum += len(chunk)
                        size_temp += len(chunk)
                        time_t = time.time() - starttime
                        if time_t > 1:
                            starttime = time.time()
                            p = (size_sum / int(siza_all)) * 100
                            speed = size_temp / time_t / 1024
                            self.show_result(filename, p, speed)
                            size_temp = 0
                self.show_result(filename, 100)
                self.new_file.append(url)

    def show_result(self, name, p, speed=None):
        if speed:
            print(now() + " [" + name + "] %.2f" % (p) + "%" + "  Speed:%.2f K/S" % (speed))
        else:
            print(now() + " [" + name + "] %.2f" % (p) + "%" + " 下载完成")

    def show_message(self):
        print("全部下载完成,文件位置:{}".format(self.dir))
        print("新增文件{}个:".format(len(self.new_file)))
        for item in self.new_file:
            print(item)

    def run(self, if_dir):
        self.go_next_dir(self.baseurl, if_dir)
        self.show_message()

    def get_fird_dir(self, url):
        html = self.get_html(url, is_file=False).content.decode("utf-8", "ignore")
        xpath_obj = etree.HTML(html)
        first_dir = xpath_obj.xpath("//a/@href")
        url_list = [self.baseurl + dir for dir in first_dir if dir not in self.ignore]
        return url_list


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def run(baseurl, downdir, if_dir):
    ts = TarenaSpider(baseurl, downdir)
    ts.run(if_dir)


def main():
    baseurl = "http://code.tarena.com.cn/WEBCode/wfd1905/"
    # 设置下载目录
    downdir = "/home/tarena/1905/"

    ts = TarenaSpider(baseurl, downdir)
    linkList = ts.get_fird_dir(baseurl)

    if_dir = False
    t_list = []
    for alink in linkList:
        if alink.endswith("/"):
            if_dir = True
        else:
            if_dir = False

        t = Thread(target=run, args=(alink, downdir, if_dir))
        t_list.append(t)
        t.start()

    for t in t_list:
        t.join()


main()
