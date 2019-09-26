#!/usr/bin/python
from fake_useragent import UserAgent
import requests
from lxml import etree
import re


class WebSpider:
    def __init__(self):
        self.ua = UserAgent()

    def __set_headers(self):
        self.headers = {
            "method": "GET",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cookie": "TMOOC-SESSION=5B4D98A1E4C9457A91F1E1B47600C5EB; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1569312158; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1569312158; sessionid=5B4D98A1E4C9457A91F1E1B47600C5EB|E_bfukbc1; cloudAuthorityCookie=0; versionListCookie=AIDTN201903; defaultVersionCookie=AIDTN201903; versionAndNamesListCookie=AIDTN201903N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV06N22N658321; courseCookie=AID; stuClaIdCookie=658321; tedu.local.language=zh-CN; isCenterCookie=yes; JSESSIONID=C7D4A1FBDD134252D14115DB5DD8C002; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1569312252,1569315239,1569315312,1569315602; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1569315602"
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

    def __parse_html_level2(self, name, url):
        html = self.__get_html(url).content.decode("utf-8", "ignore")
        # self.__write_file('html.txt', html.content.decode("utf-8", "ignore"))
        pattern = re.compile("<a href=.*?changeVideo\('(.*?)',this\).*?</a>", re.S)
        basename = pattern.findall(html)  # basename = ['aid19050531am.m3u8', 'aid19050531pm.m3u8']
        baseurl = "http://videotts.it211.com.cn"
        for one_name in basename:
            name = one_name.split(".")[0]
            url = "/".join([baseurl, name, one_name])
            self.__parse_html_level3(name, url)
            return

    def __parse_html_level3(self, name, url):
        print(url)
        html = self.__get_html(url)
        self.__write_file('html.txt', html.content.decode("utf-8", "ignore"))

    def run(self, base_url):
        self.__set_data()
        html = self.__get_html(base_url)
        # self.__write_file('html.txt',html.content.decode("utf-8","ignore"))
        self.__get_info(html.content.decode("utf-8", "ignore"))
        # self.__write_list_file('urls.txt',urls)

    def save_file(self,url):
        self.__set_data()
        html = self.__get_html(url)
        self.__write_file('html.txt', html.content.decode("utf-8", "ignore"))

# url = "http://tts.tmooc.cn/studentCenter/toMyttsPage"
# ws = WebSpider()
# ws.run(url)

url = "http://videotts.it211.com.cn/aid19050531am/aid19050531am-0.ts"
ws = WebSpider()
ws.save_file(url)
