#!/usr/bin/python3.6
# encoding:utf-8
# from fake_useragent import UserAgent
import requests
from lxml import etree
import re
import os
from Crypto.Cipher import AES
import time


class WebSpider:
    def __init__(self, base_dir="./", base_name="mp4"):
        # self.ua = UserAgent()
        self.download_dir = base_dir + base_name + "/"
        self.__create_dirs(self.download_dir)

    def __set_headers(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Referer": "http://tts.tmooc.cn/video/showVideo?menuId=678266&version=TSDTN201905",
            "Cookie": "tedu.local.language=zh-CN; __root_domain_v=.tmooc.cn; _qddaz=QD.4obkqa.one1si.k0yyg6co; cloudAuthorityCookie=0; _qdda=3-1.1us199; TMOOC-SESSION=36590CECE6814AED990CB55DA3887ED6; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1570584414,1570686654,1570793087,1570793570; _qddab=3-ya0g9l.k1m1xtji; isCenterCookie=yes; _qddamta_2852189568=3-0; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1570797185; sessionid=36590CECE6814AED990CB55DA3887ED6|E_bfuogu9; versionListCookie=TSDTN201905; defaultVersionCookie=TSDTN201905; versionAndNamesListCookie=TSDTN201905N22N%25E8%25BD%25AF%25E4%25BB%25B6%25E6%25B5%258B%25E8%25AF%2595%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV05N22N711538; courseCookie=TESTING; stuClaIdCookie=711538; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1570795473,1570795964,1570796282,1570797192; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1570797195; JSESSIONID=061969D098F7BB4C083462077ED602D5"
            # "Cookie": ""
        }

    def __set_headers_out(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Referer": "http://tts.tmooc.cn/video/showVideo?menuId=672192&version=AIDTN201903",
            "Cookie": "__root_domain_v=.tmooc.cn; _qddaz=QD.4obkqa.one1si.k0yyg6co; TMOOC-SESSION=36590CECE6814AED990CB55DA3887ED6; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1570584414,1570686654,1570793087,1570793570; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1570796931"
        }

    def __set_data(self):
        self.data = {
            "_": "1569316283047"
        }

    def __get_html(self, url, file=False):
        if file:
            self.__set_headers_out()
        else:
            self.__set_headers()
        return requests.get(url, headers=self.headers)

    def __create_dirs(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def __get_info(self, html):
        res = etree.HTML(html)
        steps = res.xpath('//h2[@class="headline-1"]/span/text()')
        all = res.xpath('//div[@class="course-list"]')
        url_info = {}
        for index, one in enumerate(all):
            info = one.xpath('.//li[@class="opened"]')

            for onelist in info:
                name = onelist.xpath('./p/text()')[0].strip()
                name = name.replace("\r\n", "").replace("\t", "").replace(" ", "")
                url = onelist.xpath('.//li[@class="sp"]/a/@href')[0]
                self.__parse_html_level2(steps[index], name, url)

                # return

                # url_info[name] = url

        # return url_info

    def __write_file(self, name, text):
        with open(name, "w") as f:
            f.write(text)

    def __write_list_file(self, name, text):
        context = ""
        for k in text:
            context = context + "{}={}".format(k, text[k]) + "\n"
        with open(name, "w") as f:
            f.write(context)

    def __parse_html_level2(self, steps, title, url):
        html = self.__get_html(url).content.decode("utf-8", "ignore")
        # self.__write_file('html.txt', html.content.decode("utf-8", "ignore"))
        pattern = re.compile("<a href=.*?changeVideo\('(.*?)',this\).*?</a>", re.S)
        basename = pattern.findall(html)  # basename = ['aid19050531am.m3u8', 'aid19050531pm.m3u8']
        baseurl = "http://videotts.it211.com.cn"
        i = 1
        for one_name in basename:
            name = one_name.split(".")[0]  # aid19050531am
            url = "/".join([baseurl, name, one_name])  # http://videotts.it211.com.cn/aid19050531am/aid19050531am.m3u8
            mp4_title = title + "-" + str(i)
            file_name = os.path.join(self.download_dir, steps, mp4_title + '.mp4')
            print(file_name)
            if not os.path.exists(file_name):
                self.__parse_html_level3(steps, mp4_title, name, url)
                i += 1

    def __parse_html_level3(self, steps, title, name, url):
        html = self.__get_html(url).content.decode("utf-8", "ignore")
        self.__write_file('html.txt', html)
        self.__parse_text(steps, title, name, html)

    def __parse_text(self, steps, title, name, html):
        if "#EXTM3U" not in html:
            return

        dir = self.download_dir + steps + "/" + name + "/"
        os.system(r'rm -rf %s' % dir)
        self.__create_dirs(dir)

        file_line = html.split("\n")

        try:
            key_url = ""
            for index, line in enumerate(file_line):  # 第二层
                if "#EXT-X-KEY" in line:  # 找解密Key
                    # EXT-X-KEY:METHOD=AES-128,URI="http://videotts.it211.com.cn/aid19050604am/static.key"
                    pattern = re.compile('URI="(.*?)"', re.S)
                    key_url = pattern.findall(line)[0]
                    print(key_url)

                if "EXTINF" in line:  # 找ts地址并下载
                    try:
                        ts_url = file_line[index + 1]  # 拼出ts片段的URL
                        # print(ts_url) # http://videotts.it211.com.cn/aid19050531am/aid19050531am-78.ts

                        c_fule_name = file_line[index + 1].rsplit("/", 1)[-1]
                        print(c_fule_name)  # aid19050531am-78.ts
                        c_fule_name = c_fule_name.split("-")[1].split(".")[0].zfill(4) + ".ts"

                        file_name = dir + c_fule_name

                        self.save_file(key_url, ts_url, file_name)
                    except:
                        self.__error_log(steps + "/" + title + "/" + name + "/" + c_fule_name + "\n")

            self.__merrg_ts(steps, title, dir, self.download_dir)
        except:
            pass

    def __error_log(self, text):
        with open("error.log", "a") as f:
            f.write(text)

    def __merrg_ts(self, steps, title, dir, download_dir):
        # 读取ts文件夹下所有的ts文件
        path_list = os.listdir(dir)
        # 对文件进行排序
        path_list.sort()
        # 将排序后的ts的绝对路径放入列表中
        li = [os.path.join(dir, filename) for filename in path_list]
        # 类似于[001.ts|00.2ts|003.ts]
        input_file = '|'.join(li)
        # 指定输出文件名称
        output_file = os.path.join(download_dir, steps, title + '.mp4')
        # 使用ffmpeg将ts合并为mp4
        # command = 'ffmpeg -i "concat:{}" -c copy -bsf:a aac_adtstoasc -movflags +faststart {}'
        command = 'ffmpeg -loglevel quiet -i "concat:{}" -c copy -bsf:a aac_adtstoasc -movflags +faststart {}'
        command = command.format(input_file, output_file)

        # 指行命令
        os.system(command)
        os.system(r'rm -rf %s' % dir)
        print("{} {}  OK!".format(now(), output_file))

    def run(self, base_url):
        # self.__set_data()
        html = self.__get_html(base_url)
        # self.__write_file('html.txt',html.content.decode("utf-8","ignore"))
        self.__get_info(html.content.decode("utf-8", "ignore"))
        # self.__write_list_file('urls.txt',urls)

    def save_file(self, key_url, ts_url, dowmload_dir):
        # self.__set_data()
        # key_url = "http://videotts.it211.com.cn/aid19050531am/static.key"
        res_key = self.__get_html(key_url)
        key = res_key.content
        # print(key)
        html = self.__get_html(ts_url,True)
        with open(dowmload_dir, 'ab') as f:
            cryptor = AES.new(key, AES.MODE_CBC, key)
            f.write(cryptor.decrypt(html.content))


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


url = "http://tts.tmooc.cn/studentCenter/toMyttsPage"
base_dir = "/home/tarena/1905/"
ws = WebSpider(base_dir=base_dir,base_name='TSD1906')
ws.run(url)

# url = "http://videotts.it211.com.cn/aid19050603am/aid19050603am-92.ts"
# key_url = "http://videotts.it211.com.cn/aid19050603am/static.key"
# ws = WebSpider()
# ws.save_file(key_url,url,'aid19050603am-92.ts')
