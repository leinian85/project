import requests
from fake_useragent import UserAgent
import time
from threading import Thread
import os

class UploadImg:
    def __init__(self, url):
        self.baseUrl = url
        self.auth = ("tarenacode", "code_2014")

    def set_headers(self):
        ua = UserAgent()
        self.headers = {"User-Agent": ua.random}

    def get_file(self, url):
        self.set_headers()
        res = requests.get(url, auth=self.auth, headers=self.headers, stream=True)
        return res

    def writh_file(self, d_filename, filename, url):
        try:
            with open(d_filename, 'ab') as f:
                os.path.getsize(d_filename)
                with self.get_file(url=url) as res:
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
        except Exception as e:
            print(d_filename)
            os.remove(d_filename)

    def show_result(self, name, p, speed=None):
        if speed:
            print(now() + " [" + name + "] %.2f" % (p) + "%" + "  Speed:%.2f K/S" % (speed))
        else:
            print(now() + " [" + name + "] %.2f" % (p) + "%" + " 下载完成")


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# ui = UploadImg("http://code.tarena.com.cn/AIDCode/aid1905/10_django/software/typora-setup-x64.exe")
# ui = UploadImg("http://code.tarena.com.cn/WEBCode/wfd1905/DOM/day02/videos/bs/getElements vs querySelectorAll.mov")

url_list = [
    "http://code.tarena.com.cn/AIDCode/aid1905/10_django/software/typora-setup-x64.exe",
    "http://code.tarena.com.cn/WEBCode/wfd1905/DOM/day02/videos/bs/getElements vs querySelectorAll.mov",
    "http://code.tarena.com.cn/WEBCode/wfd1905/DOM/day01/day01 pm.zip"
]


def main(url):
    ui = UploadImg(url)
    filename = ui.baseUrl.split("/")[-1]
    ui.writh_file(filename, filename, ui.baseUrl)


t_list = []
for url in url_list:
    t = Thread(target=main, args=(url,))
    t_list.append(t)
    t.start()

print("=====================================")
for t in t_list:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    t.join(100)
    print("**************************************")
