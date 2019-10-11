from fake_useragent import UserAgent
import random,re,os
import requests
from multiprocessing import Pool
from Crypto.Cipher import AES

class TudeSpider():
    # 保存所以课程信息

    # cwd = os.getcwd()  # 获取当前目录即dir目录下

    # 修改windows 目录
    # cwd = "H:\\video"

    # 修改linux 目录
    cwd = "/home/tarena/1905/"
    def __init__(self,target):
        # 课程名称
        self.target = target

        # self.url="http://videotts.it211.com.cn/%s".format(target)
        # self.url = "http://videotts.it211.com.cn/isCenter.html"
        # self.url = "http://tts.tmooc.cn/studentCenter/toMyttsPage"
    def get_headers(self,url,Cookie):
        ua = UserAgent()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
            # 'User-Agent': ua.random,
            # 'Referer': 'http://tts.tmooc.cn/video/showVideo?menuId=672192&version=AIDTN201903',
            # 'Referer': 'http://tts.tmooc.cn/studentCenter/toMyttsPage',
            'Referer': url,
            # 'Cookie': 'eBoxOpenAIDTN201903=true; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1568600940,1568603883,1568607148; cloudAuthorityCookie=0; versionListCookie=AIDTN201903; defaultVersionCookie=AIDTN201903; versionAndNamesListCookie=AIDTN201903N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV06N22N710249; courseCookie=AID; stuClaIdCookie=710249; tedu.local.language=zh-CN; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1568600975,1568603908,1568607175; TMOOC-SESSION=E6AF32BE319942958894A12477EF98BA; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1568607148; sessionid=E6AF32BE319942958894A12477EF98BA|E_bfuohrv; JSESSIONID=F271441C4E55A3D3905EFF70C0CEFFEF; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1568607492; isCenterCookie=yes',
            # 'Cookie': 'eBoxOpenAIDTN201903=true; isCenterCookie=no;tedu.local.language=zh-CN; TMOOC-SESSION=3E6E9E8A6CCB496E81E5639CFD692183; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1568352745,1568431274,1569033766; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1569033766; sessionid=3E6E9E8A6CCB496E81E5639CFD692183|E_bfuohrv; cloudAuthorityCookie=0; versionListCookie=AIDTN201903; defaultVersionCookie=AIDTN201903; versionAndNamesListCookie=AIDTN201903N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV06N22N710249; courseCookie=AID; stuClaIdCookie=710249; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1568356599,1568362100,1568431305,1569033776; JSESSIONID=28D57FDB828C2D88ACE3D2A1AF39A21C; monitor_count=2; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1569033778'
            # 'Cookie': 'eBoxOpenAIDTN201903=true; TMOOC-SESSION=77BCDD35CDEA40F7BB28781897FB2827; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1569648438; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1569648438; sessionid=77BCDD35CDEA40F7BB28781897FB2827|E_bfuohrv; cloudAuthorityCookie=0; versionListCookie=AIDTN201903; defaultVersionCookie=AIDTN201903; versionAndNamesListCookie=AIDTN201903N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV06N22N710249; courseCookie=AID; stuClaIdCookie=710249; JSESSIONID=CA96E48A8BC8D4CDEF8D3D5761DF43E7; tedu.local.language=zh-CN; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1569648455,1569648475; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1569648917; isCenterCookie=yes; __root_domain_v=.tmooc.cn; _qddaz=QD.ewjy6d.z2t27b.k134fri0; _qdda=3-1.1us199; _qddab=3-xvrn37.k134frk9; _qddamta_2852189568=3-0'
            'Cookie': Cookie
        }
        return headers


    def get_html(self,url,headers):

        # 获取html
        key = requests.get(url, headers=headers).content


        # 测试网页是否访问成功
        # print(html)


        return key

    def get_data(self,key):



        # 将主页的代码转换为从字节串 转换为 字符串
        html = key.decode()

        # 测试代码
        # print("一级页面访问成功")

        # 将课程主页代码保存下来 --> 用来分析正则
        # filename = "{}.html".format(self.target)
        # with open(filename,"w",encoding="utf8") as f:
        #     f.write(html)



        # html_re =r'.*?<span class="headline-content">(?P<chapter_name>.*?)</span>.*?<li class="opened">.*?<p>(?P<video_name>.*?)</p>.*?<ul class="course-link">.*?target="_blank".*?href="(?P<video_url>.*?)".*?</ul>'
        # 获取课程一级子目录 以及 子标题的html 代码,用做提取每节课的名称和视频网址
        html_re =r'.*?<span class="headline-content">(?P<chapter_name>.*?)</span>.*?<div class="course-menu">(.*?)</div>.*?'
        pattern = re.compile(html_re, re.S)
        directory_list = pattern.findall(html)

        # 测试代码
        # print("一级页面正则成功,获取章节内容")

        # 测试代码: 测试获取的数据是否符合要求: 获取课程一级子目录 以及 子标题的html 代码
        for directory_list_item in directory_list:
            # print("章节名称及课程html数据:",directory_list_item)
            class_dict = {}

            # 对一级目录名称进行处理
            directory_name = re.sub("\s", "", directory_list_item[0])

            # 获取每节课的名称和视频网址
            html_re =r'.*?<li class="opened">.*?<p>(?P<video_name>.*?)</p>.*?<ul class="course-link">.*?class="sp".*?href="(?P<video_url>.*?)".*?</ul>'
            pattern = re.compile(html_re, re.S)
            class_list = pattern.findall(directory_list_item[1])
            print("每节课的名称和url:",class_list)

            video_list = []
            # 对数据进行处理,获取video_name(视频名称)
            for item in class_list:
                video_name = re.sub("\s","",item[0])
                video_url = re.sub("\s","",item[1])
                # print(video_name,video_url)
                video_list.append((video_name,video_url))

            class_dict[directory_name] = video_list
            # print("规整化每节课的名称和url:",video_list)
            # print("{章节名称:[(课程视频名称,url)]}",class_dict)

            # 测试字典中保存的数据格式是否正确
            # for key,value in class_dict.items():
            #     print(key,value)

            # 访问视频网页
            self.video_html(class_dict, directory_name)




    def video_html(self,class_dict,directory_name):
        count = [0]
        for key,video in class_dict.items():
            for item in video:
                count[0] = 0
                # 视频名称
                video_name = item[0]
                # 视频访问url
                video_url = item[1]

                # 创建保存的文件夹
                # directory = '{}\{}\{}'.format(TudeSpider.cwd, self.target, directory_name)
                directory = '{}/{}/{}'.format(TudeSpider.cwd, self.target, directory_name)
                # print(directory)

                # print("访问课程播放页url:",video_url)

                # 访问视频播放页的headers
                headers = {
                    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
                    # 'Cookie': 'tedu.local.language=zh-CN; sessionid=09E045D7D99E4C88A96416E6DAC181EC|E_bfuohrv;',

                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                              'application/signed-exchange;v=b3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Cookie': 'tedu.local.language=zh-CN; __root_domain_v=.tmooc.cn; '
                              '_qddaz=QD.a7153s.s4e4n9.jzyv54d9; cloudAuthorityCookie=0; versionListCookie=AIDTN201903; defaultVersionCookie=AIDTN201903; versionAndNamesListCookie=AIDTN201903N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV06N22N710249; courseCookie=AID; stuClaIdCookie=710249; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1569806675,1570760652,1570775069,1570780253; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1570780253; TMOOC-SESSION=09E045D7D99E4C88A96416E6DAC181EC; sessionid=7F2181739DFD42F5B1A5F6CBA1BD1927|E_bfuogu9; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1569806696,1569806702,1570760670,1570780279; isCenterCookie=yes; _qdda=3-1.1us199; _qddab=3-sfhqqp.k1lw54ft; JSESSIONID=C5955373D1765D4485A88C965AFB5DF1; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1570783851',
                    'Host': 'tts.tmooc.cn',
                    # 'Referer': 'http://tts.tmooc.cn/studentCenter/toMyttsPage',
                    # 'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
                }

                # 调用网页访问函数: get_html, 获取从视频播放页访问下来的数据
                html_btype = self.get_html(video_url,headers)
                # print(html_btype)
                # 对数据进行数据类型转换
                key_str = html_btype.decode()
                # print(key_str)

                # 获取视频播放页的网页数据
                filename = "{}.html".format(video_name)
                with open(filename,"w",encoding='utf8') as f:
                    f.write(key_str)

                # 对数据进行正则,获取.m3u8 的关键字
                html_re = r'.*?onclick="changeVideo\(\'(.*?)\',this\).*?'
                pattern = re.compile(html_re, re.S)

                # 获取视频网页的m3u8
                video_m3u8 = pattern.findall(key_str)
                print(video_m3u8)

                # 获取当前访问的服务器,
                # video_server = ["c.it211.com.cn","videotts.it211.com.cn"](校外服务器,校内服务器)
                html_re = r'.*?videoBase =.*?"(.*?)";.*?'
                pattern = re.compile(html_re, re.S)
                video_server = pattern.findall(key_str)
                # print(video_server)
                # print(video_m3u8)
                for m3u8 in video_m3u8:
                    # 创建合并后的视频文件名
                    # print(video_name)
                    filename2 = directory + "/" + video_name + "-" + str(count[0]) + ".mp4"
                    filename2 = filename2.replace("()","")
                    # 如果存在就跳过
                    if os.path.exists(filename2):
                        print(filename2 + ": 文件以存在")
                        count[0] += 1
                        continue

                    # 获取上下午标志
                    today = m3u8.split(".")[0][-2:]
                    # print("时间:",today)
                    # url:http://videotts.it211.com.cn/aid19050531am/static.key
                    url= video_server[1] + m3u8.split(".")[0] + "/static.key"
                    # print("解密key url:",url)

                    # 获取解密的key
                    headers = {
                        'Host': 'videotts.it211.com.cn',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
                        'Accept': '*/*',
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Accept-Encoding': 'gzip, deflate',
                        'Origin': 'http://tts.tmooc.cn',
                        'Connection': 'keep-alive',
                        'Referer': 'http://tts.tmooc.cn/video/showVideo?menuId=672192&version=AIDTN201903',
                    }
                    decryption_key = self.get_html(url,headers)

                    # url = "http://videotts.it211.com.cn/aid19050603am/aid19050603am.m3u8"
                    url= video_server[1] + m3u8.split(".")[0] + "/" + m3u8
                    print(url)

                    # 获取.m3u8 网页的headers
                    headers = {
                        # 校内服务器
                        'Host': 'videotts.it211.com.cn',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
                        'Accept': '*/*',
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Accept-Encoding': 'gzip, deflate',
                        'Origin': 'http://localhost:63342',
                        'Connection': 'keep-alive',
                        'Referer': 'http://tts.tmooc.cn/video/showVideo?menuId=672192&version=AIDTN201903',
                        'Cache-Control': 'max-age=0',

                        # 校外服务器
                        # 'Host': 'c.it211.com.cn',
                        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
                        # 'Accept': '*/*',
                        # 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        # 'Accept-Encoding': 'gzip, deflate',
                        # 'Origin': 'http://localhost:63342',
                        # 'Connection': 'keep-alive',
                        # 'Referer': 'http://localhost:63342/spider/htm2.html?_ijt=agi1bundr7hfen5gm00q2k9edh',
                        # 'Cache-Control': 'max-age=0',
                    }

                    # 访问: .m3u8网页
                    html_btype = self.get_html(url, headers)
                    key_str = html_btype.decode()
                    # print(key_str)

                    # 存储.m3u8文件
                    # filename = "{}_m3u8.txt".format(self.target)
                    # with open(filename,"w",encoding="utf8") as f:
                    #     f.write(key_str)

                    # 正则.m3u8 文件中的数据,获取.ts 文件的url
                    # 存储 .ts 的url
                    html_re = r'.*?#EXTINF:.*?(http:.*?)\n.*?'
                    pattern = re.compile(html_re, re.S)
                    # type(tsUrl): list
                    tsUrl = pattern.findall(key_str)

                    # 测试: 测试.ts url 测试格式是否正确
                    # for item in  tsUrl:
                    #     print(item)

                    # print("ok")


                    #创建IO多路复用
                    pool = Pool(20)

                    # 获取每个.ts 的url
                    for url in tsUrl:
                        # self.mission(url, decryption_key, headefilename2rs, directory)
                        # 视频url
                        # url = "http://videotts.it211.com.cn/aid19050531am/aid19050531am-0.ts"
                        pool.apply_async(self.mission, (url, decryption_key, headers, directory))
                    pool.close()
                    pool.join()
                    self.merge_mp4(directory,filename2,count)


    def mission(self,url, decryption_key, headers, directory):
        # 获取 .ts 网页数据
        # print(url)
        response = requests.get(url, headers=headers, stream=True)
        # print(url)

        cryptor = AES.new(decryption_key, AES.MODE_CBC, decryption_key)

        # print(directory)
        # 如果电影名路径不存在则先创建

        directory = directory + "/test"
        if not os.path.exists(directory):
            os.makedirs(directory)
            # print(1)


        # 对文件命名
        # filename = directory + "\\" + url.split("/")[-1]
        number = url.split("/")[-1].split("-")[1].split(".")[0]
        number = "%03d"%(int(number))
        # print(number)

        filename3 = "{}/{}.ts".format(directory,number)
        # print(filename3)

        # 判断文件是否存在,存在就跳过
        # if os.path.exists(filename):
        #     return


        with open(filename3, "wb") as f:
            f.write(cryptor.decrypt(response.content))
        print(filename3, "is ok")

    def merge_mp4(self,directory,filename2,count):
        """
        Linux下将.ts文件合并为.MP4文件
        :return:
        """
        # ts文件绝对路径

        # print(count[0])

        directory1 = directory + "/test"
        # print(directory1)
        count[0] += 1
        # print(filename2)
        # 读取ts文件夹下所有的ts文件
        path_list = os.listdir(directory1)
        # 对文件进行排序
        path_list.sort()
        # 将排序后的ts的绝对路径放入列表中
        li = [os.path.join(directory1, filename) for filename in path_list]
        # 类似于[001.ts|00.2ts|003.ts]
        input_file = '|'.join(li)
        # 指定输出文件名称
        # output_file = ts_path + '.mp4'
        # 使用ffmpeg将ts合并为mp4
        # command = 'ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc %s' % (input_file, output_file)
        # command = r"copy /b %s\*.ts %s\%s.mp4" % (ts_path, ts_path,filename2, )
        command = 'ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc %s' % (input_file, filename2)
        # 指行命令
        os.system(command)
        # os.system(r"del  %s\*.ts" % (ts_path))
        os.system(r'rm -rf %s/*.ts'%(directory1))


    def before_merge(self,directory,video_name,today):
        ts_path = directory
        filename = directory + "\{}{}".format(video_name, today)
        # print("------------------------current working directory------------------" + filename)
        os.system(r"copy /b %s\*.ts %s.mp4" %(ts_path,filename))
        os.system(r"del  %s\*.mp4"%(ts_path))
if __name__ == "__main__":

    target = "tsd1906"
    url = "http://tts.tmooc.cn/studentCenter/toMyttsPage"
    # 创建TudeSpider 类的实例对象
    ts = TudeSpider(target)

    # 进入课程首页Cookie
    Home_Cookie = "eBoxOpenAIDTN201903=true; TMOOC-SESSION=77BCDD35CDEA40F7BB28781897FB2827; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1569648438; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1569648438; sessionid=77BCDD35CDEA40F7BB28781897FB2827|E_bfuohrv; cloudAuthorityCookie=0; versionListCookie=AIDTN201903; defaultVersionCookie=AIDTN201903; versionAndNamesListCookie=AIDTN201903N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV06N22N710249; courseCookie=AID; stuClaIdCookie=710249; JSESSIONID=CA96E48A8BC8D4CDEF8D3D5761DF43E7; tedu.local.language=zh-CN; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1569648455,1569648475; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1569648917; isCenterCookie=yes; __root_domain_v=.tmooc.cn; _qddaz=QD.ewjy6d.z2t27b.k134fri0; _qdda=3-1.1us199; _qddab=3-xvrn37.k134frk9; _qddamta_2852189568=3-0"

    # 获取headers
    # headers=ts.get_headers(url,Home_Cookie)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Cookie': 'tedu.local.language=zh-CN; sessionid=7F2181739DFD42F5B1A5F6CBA1BD1927|E_bfuogu9;',
    }

    # 访问网页,获取网页数据
    key = ts.get_html(url,headers)
    # print(key)


    # 解析数据,获取课程名称和视频网址
    print(1)
    ts.get_data(key)
    print(2)
    # print(video_list)

    # # 访问视频网页
    # html = ts.video_html(video_list,directory_name,count=0)

