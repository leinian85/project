# -*- coding: utf-8 -*-

	# url = "http://videotts.it211.com.cn/aid19020425am/aid19020425am-%d.ts"%n
	# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
	# "Referer": "http://tts.tmooc.cn/video/showVideo?menuId=646465&version=AIDTN201809",
	# "Cookie":"tedu.local.language=zh-CN; cloudAuthorityCookie=0; \
	# versionListCookie=AIDTN201809; \
	# defaultVersionCookie=AIDTN201809; \
	# versionAndNamesListCookie=AIDTN201809N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV05; courseCookie=AID; stuClaIdCookie=673505; \
	# Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1556238324,1556239545,1556272968,1556328972; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1556328972; \
	# TMOOC-SESSION=0C82D332A896490E9175E96700293A79; \
	# sessionid=0C82D332A896490E9175E96700293A79|E_bfummff;\
	# isCenterCookie=yes;\
	# Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1556239578,1556272984,1556280681,1556329002; \
	# JSESSIONID=F2A4E5C230A8C7A425EFA68F8495B8F7; \
	# Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1556329008"}

import requests
from multiprocessing import Pool
from Crypto.Cipher import AES
import os
import time,random
from fake_useragent import UserAgent


ua = UserAgent()

def mission(url,n,key,headers,date):
    response=requests.get(url,headers=headers,stream=True)
    cryptor = AES.new(key, AES.MODE_CBC, key)

    # 创建保存的文件名
    # /home/tarena/Python_artificial_intelligence/1905/spider/day02/static/tp100
    directory = '/home/tarena/images/{}/'.format(date)
    # 如果电影名路径不存在则先创建
    if not os.path.exists(directory):
        os.makedirs(directory)
        # print(1)

    filename = directory + "%03d.ts"%n
    # 判断文件是否存在
    # if os.path.exists(filename):
    #     return
    # else:
    with open(filename, "wb") as f:
        f.write(cryptor.decrypt(response.content))
    print (date,n,"is ok")


def before_merge(date):
    """
    Windows下将ts文件合并为.mp4文件,地址配置错误,需重新配置
    :param date:
    :return:
    """
    cwd = os.getcwd()  # 获取当前目录即dir目录下
    print("------------------------current working directory------------------" + cwd)
    os.system(r"copy /b MP4\*.mp4 MP5\%s.mp4"%date)
    os.system(r"del  MP4\*.mp4")

def merge_mp4(date):
    """
    Linux下将.ts文件合并为.MP4文件
    :return:
    """
    # ts文件绝对路径
    ts_path = '/home/tarena/images/{}'.format(date)
    # 读取ts文件夹下所有的ts文件
    path_list = os.listdir(ts_path)
    # 对文件进行排序
    path_list.sort()
    # 将排序后的ts的绝对路径放入列表中
    li = [os.path.join(ts_path, filename) for filename in path_list]
    # 类似于[001.ts|00.2ts|003.ts]
    input_file = '|'.join(li)
    # 指定输出文件名称
    output_file = ts_path + '.mp4'
    # 使用ffmpeg将ts合并为mp4
    command = 'ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc %s' % (input_file, output_file)
    # 指行命令
    os.system(command)
    os.system(r'rm -rf %s'%ts_path)


def down(date,headers,target):
    # 秘钥url
    key = requests.get('http://videotts.it211.com.cn/%s%s/static.key'%(target,date), headers = headers).content
    #print(response.json.text.decode())
    print(key)
    try:
        if isinstance(key.decode(), str):
            print("no")
            return
    except:
        print("ok")
        time.sleep(5)
        pool=Pool(20)
        if date[-2] == "a":
            count= 250
        else:
            count=400
        for n in range(0,count):
            # 视频url
            url = "http://videotts.it211.com.cn/%s%s/%s%s-%d.ts"% (target,date,target, date, n)
            pool.apply_async(mission,(url,n,key,headers,date))
        pool.close()
        pool.join()
        # windows合并.ts文件
        # before_merge(date)

        # Linux下合并.ts文件
        merge_mp4(date)

if __name__ == "__main__":
    # 班级
    #target = "aid1905"
    target = "tsd1905"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Referer': 'http://tts.tmooc.cn/video/showVideo?menuId=672192&version=AIDTN201903',
        'Cookie': 'eBoxOpenAIDTN201903=true; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1568600940,1568603883,1568607148; cloudAuthorityCookie=0; versionListCookie=AIDTN201903; defaultVersionCookie=AIDTN201903; versionAndNamesListCookie=AIDTN201903N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV06N22N710249; courseCookie=AID; stuClaIdCookie=710249; tedu.local.language=zh-CN; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1568600975,1568603908,1568607175; TMOOC-SESSION=E6AF32BE319942958894A12477EF98BA; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1568607148; sessionid=E6AF32BE319942958894A12477EF98BA|E_bfuohrv; JSESSIONID=F271441C4E55A3D3905EFF70C0CEFFEF; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1568607492; isCenterCookie=yes'
    }
    # month = ("10","11","12","01","02","03","04","05","06","07","08","09")
    month = ("03","04","05","06","07","08","09","10","11","12","01","02",)
    # 开始月份
    start = 1
    # 结束月份
    end = 5
    for j in month[start+2:end+3]:
        for i in range(1, 32):
            for k in ["am", "pm"]:
                print(k)
                try:
                    print("start down %s%02d%s"%(j,i,k))
                    down("%s%02d%s"%(j,i,k), headers,target)
                    print("%s%02d%s is ok"%(j,i,k))
                except Exception as e:
                    print(e)
                    continue

                # 随机休眠
                time.sleep(random.randint(1,2))

	# videoBase：http://videotts.it211.com.cn/
