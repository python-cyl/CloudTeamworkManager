from urllib import request
from urllib import parse
from bs4 import BeautifulSoup


url = r"http://202.207.240.67:801/eportal/?c=ACSetting&a=Login&wlanuserip=null&wlanacip=null&wlanacname=null&port=&iTermType=1&mac=123456789012&ip=000.000.000.000&redirect=null"
headers = {
    "Accept": "text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8", 
    "Accept-Encoding": "gzip, deflate", 
    "Accept-Language": "zh-CN", 
    "Cache-Control": "max-age=0", 
    "Connection": "Keep-Alive", 
    "Content-Length": "49", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Cookie": "PHPSESSID=h9hqin0ol1ursnvhb18hpo6vr7; md5_login=songdingning6797%7C346191tyuT; divshowUID=songdingning6797", 
    "DNT": "1", 
    "Host": " 202.207.240.67:801", 
    "Referer": " http://202.207.240.67/a70.htm", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
    }

data = {
    "DDDDD": "songdingning6797", 
    "save_me": "1", 
    "upass": "346191tyuT"
    }

data = parse.urlencode(data).encode('utf-8')
req = request.Request(url, headers=headers, data=data)
response = request.urlopen(req).read()
response = response.decode("gbk")

soup = BeautifulSoup(response)
title = soup.find("title")
title = title.string
