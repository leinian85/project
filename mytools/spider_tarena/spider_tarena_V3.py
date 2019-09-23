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

baseurl = "http://code.tarena.com.cn/BIGCode/big1904/"
# 设置下载目录
downdir = "/home/tarena/1905/"

AUTH = ("tarenacode", "code_2014")
INGORE = ["../"]

FILESIZE = 1*1024*1024
FILESIZELIST = "downlist"

all_files_size = {}  # 记录下载过的文件大小
un_done_files = []
new_file = []

class TarenaSpider:
    def __init__(self, url, dir):
        self.baseurl = url
        self.dir = dir

    @staticmethod
    def __set_files_size_dic():
        with open(FILESIZELIST, "r") as f:
            for line in f.readlines():
                k = line.split("=")[0].strip()
                v = line.split("=")[1].strip()
                all_files_size[k] = v

    @staticmethod
    def __set_cnf():
        TarenaSpider.ua = UserAgent()

    @staticmethod
    def __write_down_list(name,size):
        text ="{}={}\n".format(name,size)
        with open(FILESIZELIST,"a") as f:
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
            html = requests.get(url=url, auth=AUTH, headers=headers, stream=True)
        else:
            print("url-dir:", url)
            html = requests.get(url=url, auth=AUTH, headers=headers)

        return html

    def go_next_dir(self, url, if_dir):
        if not if_dir:
            self.download(url)
            return

        html = self.get_html(url).content.decode("utf-8", "ignore")
        r_obj = etree.HTML(html)
        r_list = r_obj.xpath("//a/@href")
        for urlone in r_list:
            if urlone in INGORE:
                continue

            dir_one = url + urlone

            # url = "http://code.tarena.com.cn/AIDCode/aid1905/14_spider/"
            # 获取上级目录 AIDCode/aid1905/14_spider/
            is_dir = False
            if dir_one.endswith("/"):
                dir = self.dir + dir_one[26:]
                is_dir = True
            else:
                dir = self.dir + "/".join(dir_one[26:].split("/")[:-1])
                is_dir = False

            if not os.path.exists(dir):
                os.makedirs(dir)

            self.go_next_dir(dir_one, is_dir)
            # time.sleep(random.randint(1, 3))

    # 下载文件
    def download(self, url):
        filename = self.dir + "/".join(url.split("://")[1].split("/")[1:])
        name = url.split("/")[-1]
        file_size = int(all_files_size.get(filename, "0"))
        if_continue = False
        # 判断是否需要续传,大于等于配置的大小就需要续传
        if file_size >= FILESIZE:
            if_continue = True

        if os.path.exists(filename):
            local_file_size = int(os.path.getsize(filename))
        else:
            local_file_size = 0

        if if_continue:
            # 判断需要续传的文件是否下载完成
            if local_file_size == file_size:
                return
        else:
            # 判断不需要续传的文件是否存在
            if os.path.exists(filename):
                return

        self.writh_file(filename, name, url, local_file_size)

    # 写入文件
    def writh_file(self, d_filename, filename, url, local_file_size):
        '''
        :param d_filename: 文件的下载路径
        :param filename: 文件名
        :param url: 文件下载的url
        '''


        if_continue = False
        try:
            with open(d_filename, 'ab') as f:
                with self.get_html(url=url, is_file=True, size=local_file_size) as res:
                    siza_all = int(res.headers.get("Content-Length"))
                    if siza_all >= FILESIZE:
                        if_continue = True
                        TarenaSpider.__write_down_list(d_filename,siza_all)
                    else:
                        # 记录不续传的文件,下载异常的要删除
                        un_done_files.append(d_filename)
                    size_sum = local_file_size
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
                    new_file.append(url)

                    if not if_continue:
                        un_done_files.remove(d_filename)
        except:
            pass

    def show_result(self, name, p, speed=None):
        if speed:
            print(now() + " [" + name + "] %.2f" % (p) + "%" + "  Speed:%.2f K/S" % (speed))
        else:
            print(now() + " [" + name + "] %.2f" % (p) + "%" + " 下载完成")

    def show_dir(self):
        print("下载完成,文件位置:{}".format(self.dir))

    def show_message(self):
        print("新增文件{}个:".format(len(new_file)))
        for item in new_file:
            print(item)

    def run(self, if_dir):
        self.go_next_dir(self.baseurl, if_dir)

    def get_fird_dir(self, url):
        html = self.get_html(url, is_file=False).content.decode("utf-8", "ignore")
        xpath_obj = etree.HTML(html)
        first_dir = xpath_obj.xpath("//a/@href")
        url_list = [self.baseurl + dir for dir in first_dir if dir not in INGORE]
        return url_list


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def run(baseurl, downdir, if_dir):
    print("{} 开始提取...".format(baseurl))
    ts = TarenaSpider(baseurl, downdir)
    ts.run(if_dir)
    print("{} 提取完成.".format(baseurl))

def run_one_dir():
    ts = TarenaSpider(baseurl, downdir)

    try:
        ts.data_init()
        ts.run(True)
        ts.show_dir()
        ts.show_message()

        if un_done_files:
            print("正在删除未下载完成的文件...")
            for file in un_done_files:
                os.remove(file)
    except Exception as e:
        ts.show_message()
        if un_done_files:
            print("正在删除未下载完成的文件...")
            for file in un_done_files:
                os.remove(file)
        print("程序终止")

def main():
    ts = TarenaSpider(baseurl, downdir)
    ts.data_init()
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

        if un_done_files:
            print("正在删除未下载完成的文件...")
            for file in un_done_files:
                os.remove(file)
    except Exception as e:
        print(e)
        if un_done_files:
            print("正在删除未下载完成的文件...")
            for file in un_done_files:
                os.remove(file)
        print("程序终止")


main()
# run_one_dir()
