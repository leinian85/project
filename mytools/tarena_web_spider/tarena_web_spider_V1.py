#!/usr/bin/python
from fake_useragent import UserAgent
import requests
from lxml import etree
import re
import os
from Crypto.Cipher import AES


class WebSpider:
    def __init__(self, base_dir="./", base_name="mp4"):
        self.ua = UserAgent()
        self.download_dir = base_dir + base_name + "/"
        self.__create_dirs(self.download_dir)

    def __set_headers(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Referer": "http://tts.tmooc.cn/video/showVideo?menuId=672192&version=AIDTN201903",
            "Cookie": "tedu.local.language=zh-CN; __root_domain_v=.tmooc.cn; _qddaz=QD.4obkqa.one1si.k0yyg6co; cloudAuthorityCookie=0; versionListCookie=AIDTN201903; defaultVersionCookie=AIDTN201903; versionAndNamesListCookie=AIDTN201903N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV06N22N658321; courseCookie=AID; stuClaIdCookie=658321; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1569396919,1569544618; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1569544618; TMOOC-SESSION=D4D64B305AE74825A3427E0C92223E14; sessionid=D4D64B305AE74825A3427E0C92223E14|E_bfukbc1; isCenterCookie=yes; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1569396937,1569498174,1569544623; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1569544635; _qdda=3-1.1us199; _qddab=3-ild3b0.k11ecn8q; _qddamta_2852189568=3-0; JSESSIONID=189FF721AE1E09E15DDA9B1EEA2EFB0D"
        }

    def __set_data(self):
        self.data = {
            "_": "1569316283047"
        }

    def __get_html(self, url, file=False):
        self.__set_headers()

        if file:
            return requests.get(url, data=self.data, headers=self.headers, stream=True)
        return requests.get(url, data=self.data, headers=self.headers)

    def __create_dirs(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def __get_info(self, html):
        res = etree.HTML(html)
        all = res.xpath('//div[@class="course-list"]')
        url_info = {}
        for one in all:
            info = one.xpath('.//li[@class="opened"]')

            for onelist in info:
                name = onelist.xpath('./p/text()')[0].strip()
                name = name.replace("\r\n", "").replace("\t", "").replace(" ", "")
                url = onelist.xpath('.//a/@href')[0]

                self.__parse_html_level2(name, url)

                return

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

    def __parse_html_level2(self, title, url):
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
            if not os.path.exists(os.path.join(self.download_dir, mp4_title + '.mp4')):
                self.__parse_html_level3(mp4_title, name, url)
                i += 1

    def __parse_html_level3(self, title, name, url):
        html = self.__get_html(url).content.decode("utf-8", "ignore")
        self.__parse_text(title, name, html)
        # self.__write_file('html.txt', html.content.decode("utf-8", "ignore"))

    def __parse_text(self, title, name, html):
        if "#EXTM3U" not in html:
            return

        dir = self.download_dir + name + "/"
        self.__create_dirs(dir)

        file_line = html.split("\n")

        for index, line in enumerate(file_line):  # 第二层
            if "#EXT-X-KEY" in line:  # 找解密Key
                method_pos = line.find("METHOD")
                comma_pos = line.find(",")
                method = line[method_pos:comma_pos].split('=')[1]

                # "Decode Method：", method

                uri_pos = line.find("URI")
                quotation_mark_pos = line.rfind('"')
                key_path = line[uri_pos:quotation_mark_pos].split('"')[1]

                key_url = key_path  # 拼出key解密密钥URL
                res = self.__get_html(key_url)
                key = res.content
                cryptor = AES.new(key, AES.MODE_CBC, key)

            if "EXTINF" in line:  # 找ts地址并下载
                ts_url = file_line[index + 1]  # 拼出ts片段的URL
                # print(ts_url) # http://videotts.it211.com.cn/aid19050531am/aid19050531am-78.ts

                c_fule_name = file_line[index + 1].rsplit("/", 1)[-1]
                print(c_fule_name) # aid19050531am-78.ts

                res = self.__get_html(ts_url)
                file_name = dir + c_fule_name
                with open(file_name, 'ab') as f:
                    f.write(cryptor.decrypt(res.content))

        self.__merrg_ts(title, dir, self.download_dir)

    def __merrg_ts(self, title, dir, download_dir):
        # 读取ts文件夹下所有的ts文件
        path_list = os.listdir(dir)
        # 对文件进行排序
        path_list.sort()
        # 将排序后的ts的绝对路径放入列表中
        li = [os.path.join(dir, filename) for filename in path_list]
        # 类似于[001.ts|00.2ts|003.ts]
        input_file = '|'.join(li)
        # 指定输出文件名称
        output_file = os.path.join(download_dir, title + '.mp4')
        # 使用ffmpeg将ts合并为mp4
        # command = 'ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc %s' % (input_file, output_file)
        command = 'ffmpeg -loglevel quiet -i "concat:{}" -c copy -bsf:a aac_adtstoasc -movflags +faststart {}'
        command = command.format(input_file, output_file)

        # 指行命令
        os.system(command)
        os.system(r'rm -rf %s' % dir)
        print("{}  OK!".format(output_file))

    def run(self, base_url):
        self.__set_data()
        html = self.__get_html(base_url)
        # self.__write_file('html.txt',html.content.decode("utf-8","ignore"))
        self.__get_info(html.content.decode("utf-8", "ignore"))
        # self.__write_list_file('urls.txt',urls)

    def save_file(self, url):
        self.__set_data()
        html = self.__get_html(url)
        self.__write_file('html.txt', html.content.decode("utf-8", "ignore"))


url = "http://tts.tmooc.cn/studentCenter/toMyttsPage"
base_dir = "/home/tarena/1905/"
ws = WebSpider(base_dir=base_dir)
ws.run(url)

# url = "http://videotts.it211.com.cn/aid19050531am/aid19050531am-0.ts"
# ws = WebSpider()
# ws.save_file(url)
