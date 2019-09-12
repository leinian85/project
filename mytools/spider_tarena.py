import requests
from fake_useragent import UserAgent
import os
from lxml import etree
import time
import random


class TarenaSpider:
    def __init__(self, dir, ignore=[]):
        self.classNo = "1905"
        self.auth = ("tarenacode", "code_2014")
        self.dir = dir
        self.ignore = ignore
        self.ua = UserAgent()
        self.new_file = []

    def get_html(self, url, is_file=False):

        headers = {"User-Agent": self.ua.random}
        # proxies = {
        #     "http":"http://27.204.112.20:9999",
        #     "https":"http://27.204.112.20:9999"
        # }
        if is_file:
            print("url-file:", url)
            html = requests.get(url=url, auth=self.auth, headers=headers, stream=True)
        else:
            print("url-dir:", url)
            html = requests.get(url=url, auth=self.auth, headers=headers)

        # print(html.headers)
        # {
        #  'Server': 'nginx/1.4.3',
        #  'Date': 'Thu, 12 Sep 2019 02:17:41 GMT',
        #  'Content-Type': 'text/html; charset=gbk',
        #  'Connection': 'close',
        #  'Vary': 'Accept-Encoding'
        #  }
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
                # os.mkdir(dir)
                os.makedirs(dir)

            self.go_next_dir(dir_one, is_dir)
            # time.sleep(random.randint(1, 3))

    def formatFloat(self, num):
        return '{:.2f}'.format(num)

    def download(self, url):
        filename = self.dir + url[26:]
        name = url.split("/")[-1]
        if os.path.exists(filename):
            print("{} 文件已存在".format(name))
            return

        # print(req.headers['content-length'])
        # print(req.headers)
        # {'Server': 'nginx/1.4.3',
        #  'Date': 'Thu, 12 Sep 2019 02:25:17 GMT',
        #  'Content-Type': 'application/zip',
        #  'Content-Length': '1298767',
        #  'Last-Modified': 'Wed, 11 Sep 2019 20:49:02 GMT',
        #  'Connection': 'keep-alive',
        #  'ETag': '"5d795dbe-13d14f"',
        #  'Accept-Ranges': 'bytes'
        #  }

        # res = req.content
        with open(filename, "wb") as f:
            count = 0
            count_tmp = 0
            time1 = time.time()

            with self.get_html(url, is_file=True) as res:
                # print(res.headers)
                length = float(res.headers.get('Content-Length',len(res.content)))
                for chunk in res.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
                        count += len(chunk)
                        time_t = time.time() - time1
                        if time.time() - time1 > 0.5:
                            p = count / length * 100
                            speed = (count - count_tmp) / 1024 / 1024 / time_t
                            count_tmp = count
                            print(now() + " " + name + ': ' + self.formatFloat(p) + '%' + ' Speed: ' + self.formatFloat(
                                speed)
                                  + 'M/S')
                            time1 = time.time()

            # f.write(res)
            self.new_file.append(url)
            print(now() + " " + name + ': 100% 下载完成!')


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


baseurl = "http://code.tarena.com.cn/AIDCode/aid1905/"
# 设置下载目录
downdir = "/home/tarena/1905/"
# 设置忽略文件夹
ignore = ["../"]
ts = TarenaSpider(downdir, ignore)
ts.go_next_dir(baseurl,True)
print("全部下载完成,文件位置:{}".format(downdir))
print("新增文件{}个:".format(len(ts.new_file)))
for item in ts.new_file:
    print(item)
