#!/usr/bin/python3.6
# encoding:utf-8
# from fake_useragent import UserAgent
import requests
from lxml import etree
import re
import os
from Crypto.Cipher import AES
import time
from threading import Thread


class WebSpider:
    def __init__(self, base_dir="./", base_name="mp4", valid=[]):
        # self.ua = UserAgent()
        self.download_dir = base_dir + base_name + "/"
        self.__create_dirs(self.download_dir)
        self.valid = valid
        self.dir_list_not_over = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Referer": "http://tts.tmooc.cn/video/showVideo?menuId=678266&version=TSDTN201905"
        }

    def __set_headers(self):
        self.headers["Cookie"] = \
            'tedu.local.language=zh-CN; __root_domain_v=.tmooc.cn; _qddaz=QD.4obkqa.one1si.k0yyg6co; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1572003004,1572246919,1572310413,1572345781; TMOOC-SESSION=BCF8B189748043178D60E20782A13225; isCenterCookie=yes; sessionid=BCF8B189748043178D60E20782A13225|E_bfuiscb; cloudAuthorityCookie=0; versionListCookie="NTDVN201907,,NTDTN201903"; versionAndNamesListCookie=NTDVN201907N22NNTD%25E5%258D%258E%25E4%25B8%25BA%25E8%25AE%25A4%25E8%25AF%2581%25E8%25AF%25BE%25E7%25A8%258BVIP2.0N22N741536M11MNTDTN201903N22N%25E7%25BD%2591%25E7%25BB%259C%25E8%25BF%2590%25E7%25BB%25B4%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV05N22N729317; courseCookie=NTD; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1572828414; defaultVersionCookie=NTDTN201903; stuClaIdCookie=729317; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1572345834,1572407855,1572828395,1572828425; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1572828428; _qdda=3-1.1us199; _qddab=3-clhm9e.k2jpfq2j; _qddamta_2852189568=3-0; JSESSIONID=96F6231822EC62B9635C180684091989'
        # "Cookie": ""

    def __set_headers_out(self):
        self.headers[
            "Cookie"] = "__root_domain_v=.tmooc.cn; _qddaz=QD.4obkqa.one1si.k0yyg6co; TMOOC-SESSION=36590CECE6814AED990CB55DA3887ED6; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1570584414,1570686654,1570793087,1570793570; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1570796931"

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

        t_list = []
        for index, one in enumerate(all):
            t = Thread(target=self.upload_one_dir, args=(index, one, steps))
            t_list.append(t)
            t.setDaemon(True)
            t.start()

        for t in t_list:
            t.join()

    def upload_one_dir(self, index, one, steps):
        step_ = steps[index]
        info = one.xpath('.//li[@class="opened"]')
        if (not self.valid) or (step_ in self.valid):
            print(1)
            self.dir_list_not_over.append(step_)
            step = str(index + 1).zfill(4) + '_' + step_
            print("目录:", step)
            for onelist in info:
                name = onelist.xpath('./p/text()')[0].strip()
                name = name.replace("\r\n", "").replace("\t", "").replace(" ", "").replace("/", "").replace("(",
                                                                                                            "").replace(
                    ")", "").replace('、', '').replace('：', '_').replace('（', '').replace('）', '')
                url = onelist.xpath('.//li[@class="sp"]/a/@href')[0]

                self.__parse_html_level2(step, name, url)

        if step_ in self.dir_list_not_over:
            self.dir_list_not_over.remove(step_)

    def __write_file(self, name, text):
        with open(name, "w") as f:
            f.write(text)

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

            if not os.path.exists(file_name):
                print("文件名:", file_name)
                self.__parse_html_level3(steps, mp4_title, name, url)
            i += 1


    def __parse_html_level3(self, steps, title, name, url):
        html = self.__get_html(url).content.decode("utf-8", "ignore")
        # self.__write_file('html.txt', html)
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
                    # URI="http://videotts.it211.com.cn/aid19050604am/static.key"
                    pattern = re.compile('URI="(.*?)"', re.S)
                    key_url = pattern.findall(line)[0]

                if "EXTINF" in line:  # 找ts地址并下载
                    try:
                        ts_url = file_line[index + 1]  # 拼出ts片段的URL
                        # print(ts_url) # http://videotts.it211.com.cn/aid19050531am/aid19050531am-78.ts

                        c_fule_name = file_line[index + 1].rsplit("/", 1)[-1]  # aid19050531am-78.ts
                        print("ts文件:", c_fule_name)
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
            f.write(now() + " " + text)

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
        if self.dir_list_not_over:
            self.__write_file("dir_list_not_over", str(self.dir_list_not_over))

    def save_file(self, key_url, ts_url, dowmload_dir):
        # self.__set_data()
        # key_url = "http://videotts.it211.com.cn/aid19050531am/static.key"
        res_key = self.__get_html(key_url)
        key = res_key.content
        html = self.__get_html(ts_url, True)
        with open(dowmload_dir, 'ab') as f:
            cryptor = AES.new(key, AES.MODE_CBC, key)
            f.write(cryptor.decrypt(html.content))

    def __write_list(self, text):
        with open('url_list', 'a') as f:
            f.write(text)


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


valid_list = []
url = "http://tts.tmooc.cn/studentCenter/toMyttsPage"
base_dir = "/home/tarena/1905/move/"
ws = WebSpider(base_dir=base_dir, base_name='NTD1907', valid=valid_list)
ws.run(url)

# url = "http://videotts.it211.com.cn/aid19050603am/aid19050603am-92.ts"
# key_url = "http://videotts.it211.com.cn/aid19050603am/static.key"
# ws = WebSpider()
# ws.save_file(key_url,url,'aid19050603am-92.ts')
