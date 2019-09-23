#!/usr/bin/python3

'''
    V2 : 超过一定大小的文件实现断点续传
'''
import requests
from fake_useragent import UserAgent
import os
from lxml import etree
import time
from threading import Thread
from spider_tarena1 import *


class TarenaSpider:
    all_files_size = {}  # 记录下载过的文件大小
    un_done_files = []
    new_file = []

    def __init__(self, url, dir):
        self.baseurl = url
        self.dir = dir

    @staticmethod
    def __set_files_size_dic():
        with open(config.FILESIZELIST, "r") as f:
            for line in f.readlines():
                k = line.split("=")[0].strip()
                v = line.split("=")[0].strip()
                TarenaSpider.all_files_size[k] = v

    @staticmethod
    def __set_cnf():
        TarenaSpider.ua = UserAgent()

    @staticmethod
    def __write_down_list(name,size):
        text ="{}={}\n".format(name,size)
        with open(config.FILESIZELIST,"a") as f:
            f.write(text)

    # 初始化公用配置
    def data_init(self):
        self.__set_files_size_dic()
        self.__set_cnf()

    def get_html(self, url, is_file=False, size=0):
        headers = {"User-Agent": TarenaSpider.ua.random}

        if is_file:
            headers["Range"] = 'bytes=%d-' % size
            print("url-file:", url)
            html = requests.get(url=url, auth=TarenaSpider.auth, headers=headers, stream=True)
        else:
            print("url-dir:", url)
            html = requests.get(url=url, auth=TarenaSpider.auth, headers=headers)

        return html

    def go_next_dir(self, url, if_dir):
        if not if_dir:
            self.download(url)
            return

        html = self.get_html(url).content.decode("utf-8", "ignore")
        r_obj = etree.HTML(html)
        r_list = r_obj.xpath("//a/@href")
        for urlone in r_list:
            if urlone in TarenaSpider.ignore:
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
        file_size = TarenaSpider.all_files_size.get(name, 0)
        if_continue = False
        # 判断是否需要续传,大于等于配置的大小就需要续传
        if file_size >= config.FILESIZE:
            if_continue = True

        local_file_size = os.path.getsize(name)

        if if_continue:
            # 判断需要续传的文件是否下载完成
            if local_file_size == file_size:
                return
        else:
            # 判断不需要续传的文件是否存在
            if os.path.exists(filename):
                return

        self.writh_file(filename, name, url, local_file_size, if_continue)

    # 写入文件
    def writh_file(self, d_filename, filename, url, local_file_size, if_continue):
        '''
        :param d_filename: 文件的下载路径
        :param filename: 文件名
        :param url: 文件下载的url
        '''
        # 记录不续传的文件,下载异常的要删除
        if not if_continue:
            self.un_done_files.append(d_filename)

        try:
            with open(d_filename, 'ab') as f:
                with self.get_html(url=url, is_file=True, size=local_file_size) as res:
                    siza_all = res.headers.get("Content-Length")
                    if if_continue:
                        TarenaSpider.__write_down_list(d_filename,siza_all)
                    size_sum = 0
                    size_temp = 0
                    starttime = time.time()
                    for chunk in res.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            if if_continue:
                                f.flush()
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

            if not if_continue:
                self.un_done_files.remove(d_filename)
        except:
            pass

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

    def get_fird_dir(self, url):
        html = self.get_html(url, is_file=False).content.decode("utf-8", "ignore")
        xpath_obj = etree.HTML(html)
        first_dir = xpath_obj.xpath("//a/@href")
        url_list = [self.baseurl + dir for dir in first_dir if dir not in TarenaSpider.ignore]
        return url_list


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def run(baseurl, downdir, if_dir):
    print("{} 开始提取...".format(baseurl))
    ts = TarenaSpider(baseurl, downdir)
    ts.run(if_dir)
    print("{} 提取完成.".format(baseurl))


def main():
    baseurl = "http://code.tarena.com.cn/BIGCode/big1904/04-Linux/day02/"
    # 设置下载目录
    downdir = "./"

    ts = TarenaSpider(baseurl, downdir)
    try:
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

        ts.show_message()

        if ts.un_done_files:
            print("正在删除未下载完成的文件...")
            for file in ts.un_done_files:
                os.remove(file)
    except:
        if ts.un_done_files:
            print("正在删除未下载完成的文件...")
            for file in ts.un_done_files:
                os.remove(file)
        print("程序终止")


main()
