import  requests
from fake_useragent import UserAgent
import os
url = "http://attach.bbs.miui.com/forum/201403/25/145416j7tqtdztq6aaa6p6.jpg"
ua = UserAgent()
if os.path.exists("1.jpg"):
    local_size = int(os.path.getsize("1.jpg"))
else:
    local_size = 0
headers = {"User-Agent":ua.random,"Range":"bytes=%d-"%local_size}
with open("1.jpg","ab") as f:
    with requests.get(url=url,headers = headers,stream=True) as res:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                # break


