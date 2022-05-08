# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:13:13 2021
@author: wy
@user_now: chen yq
"""

# 本程序旨在解决钉钉打卡问题，拟输出成程序并直接运行
# 目前考虑有两种路线，一种是Chromedriver模拟点击，一种是参看是否可用requests库解决
# 参考代码：https://github.com/lgaheilongzi/ZJU-Clock-In#readme
import requests
import re
import time
import datetime
import json
import ddddocr


def get_code(session, headers):
    # 获取验证码
    url_code = 'https://healthreport.zju.edu.cn/ncov/wap/default/code'
    ocr = ddddocr.DdddOcr()
    # resp = session.get(url_code)
    resp = session.get(url_code, headers=headers)
    code = ocr.classification(resp.content)
    return code


def get_date():
    """Get current date"""
    today = datetime.date.today()
    return "%4d%02d%02d" % (today.year, today.month, today.day)


def deal_person1():
    url_save = 'https://healthreport.zju.edu.cn/ncov/wap/default/save'
    url_index = 'https://healthreport.zju.edu.cn/ncov/wap/default/index'

    # 给出headers和cookies，令其可以免登录
    # headers和cookies的确定方法为：
    # 1. Chrome打开无痕页面，键入url_save网址，返回登录界面
    # 2. 右键审查元素或者按F12，找到network栏
    # 3. 输入账号密码并登录，然后找到“index”的“requests headers”一栏
    # 4. 将cookie中的所有内容全部复制粘贴到cookies = ‘’中，用以完成请求头。
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
    # cookies = 'eai-sess=a5cbru7g68sardqreor52ab0t0; UUkey=7845ce9dc936a6d37999dbca0b2153d6; _csrf=S8mwplVi9KWoF2WQ0TlCeATS6Si1PggMUPFi597fxEc=; _pv0=Zrjx4/6YuzJ3ath/vldxxLaOnhO5A20bj2PtedSBu92cvDMiQhaIA17zuZlDs2HHTWsS46uU5eM/6Yvwg+uF2642i7QQZq+cCyfC5cwYTGFPE/3fuyVIB3NyUnaaRKZoTK5HnO1k/i8iEQ6R8qsX8hanimrrrKxaikSu8Jj1iR4P8W89hxmcPE+/TSNlT0yIPIWpW/Xdxi/UQZk+exj197kAkp0JGWPav4SNhvZ/7kKebGrCnydtw8nQ19dHhIbuIQXapWEnLCCQ56yH7ik8fiM0L8Oc+Vdv/VYJD0WkjnVummjoq+6pBLhirVo+PVe+cHBhN6zSantf82WtyfB6dhk25093zwf+lq+YPrKRhu9Dr6Iv8BUCOyW/f6XiQyD2Toj1WqP8zzMGJuW9imrQWiW80fgwZ7VuTKgp9JMZSbg=; _pf0=klR3aDgwcFiknVJFRJ5KOOPRwidlBTKOWa3UqDg0XxI=; _pc0=nDHfD57vgXJDQjAw01OLDxDjyuFdg0c+aqa/4/YZ2dE=; iPlanetDirectoryPro=OHyAD7+SeUWl7JXCHo2Ppb/ba/1yNcimhNR2455jB0Nw1sDlQxZZq6XUTpGZYdqSJSAFNLTIlbLZnuuJYEr/WFxinJ58op1o81O/YXaLhz3G1CjLVU0wiqUWeO1y8NPC1Ov9IT63cm7ggIR+0ObH1fjAaSRl8C8foUMTI2CYAVtXD0mmlflVe1b4nSC3g2UVzr3hJz9qCf2KOQYrJ2SKBhxxwv0M3eamJqaaS2gznJmIgOiv2VkXZm8if4oMRxuo0jzy1yuk/mFTDVzBTCleWsvzkmSMoBxhqhd2XWa2Bnlo/DRaov1uEnJIZPZByk1ArID36A2Wnqwo47Jwb+Li65wDDQlIFvpyOGkGXB8+Epo='
    cookies = 'eai-sess=s43ukd3fd9oc4e3i2k772lvgl3; UUkey=22345a47c0395a875fe423f1258951c0; _csrf=S8mwplVi9KWoF2WQ0TlCeFvchU8QXV/PGu4F83Z+MFg=; _pv0=fNvaYinSv5mcgi22J46b0lxxXH5S6s3WlRbJtElrT+hd7HHg1lsyONRSXSKlyr5fbln1/p2s7AK6FzWEyzDgkwdf8rRxC3sd+DSbzfMzUGqCDElgdvTNU+sjTWP4rw3ipQSee3vGSsYsonqsL9nQdxrZcNTKS7Q3vlPM4B9Nd2nV3BpzSQz/a+s2CsMyvROpezm5GiL6BIUXaz9gMRfW28yB6sEK1F5yup2J0mCozsqhgFMKB8RL9J5X2V+phDeRoj3ogM0JD6+ywBfrGJ90a0jaxfaXm+6SN42EhMceliYYSwXZ5KNo6bBESo8sckddd0DbmG+hwkDcu+w7tIv5BQOAtLnTuolzHUO+hcem3MmRWB3x264cC8m6f68MPJmjGqhEHJR+uE11sv9wk8/H9jkTinRyXf5xd25s74B5wJs=; _pf0=YZ7jW0OVA421X7ReuJ11755KSTr97rzqpENZeqYIaR8=; _pc0=TdTuS/SDddqtoCODWR1rYmvoBPqfs+YGeDtbrQvkB6c=; iPlanetDirectoryPro=Ez/O3PHMXacR7jCLEuWH1EGItZvgfn4SOg35FsEQ4605tDeTHB4y3DrAF1Vz7Iqh6sjtLb28UJh2P7xZ+JVYsuzIdkiA8IUqdRz0IyRV2tjHZ9WRjSlKkw6RoF+x/xfkK5zV8DYtcYiUTOiyvKBIH9kCj4hFP4CSH3CJYANsxvHYuGNan+93uZOHqO+J4cbtQCYf+XvTDUF4C5QSL3V0R7P+kMVlRy9MZtiEQHy7GEMLe+lXizI0DLpRmAU1tjqTgjpahDp0c75ulwhkc1eHTS/g6J7Vr7b72ocelADS8/+b6j/Gjs0lUJmyJQsD3fnEH329kNqPxgrJvV9E/N7E9h/LHslYUA5VmqzVtQ/cOPg='
    cookies_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookies.split("; ")}

    # 获取session requests
    session = requests.Session()

    # 存储cookies信息到session中
    s_cookies_stored = requests.utils.add_dict_to_cookiejar(session.cookies, cookies_dict)

    r = session.get(url_index, headers=headers)
    html = r.content.decode()

    # 填表
    old_infos = re.findall(r'oldInfo: ({[^\n]+})', html)
    old_info = json.loads(old_infos[0])
    new_info_tmp = json.loads(re.findall(r'def = ({[^\n]+})', html)[0])
    new_id = new_info_tmp['id']
    name = re.findall(r'realname: "([^\"]+)",', html)[0]
    number = re.findall(r"number: '([^\']+)',", html)[0]

    new_info = old_info.copy()

    new_info['id'] = new_id
    new_info['name'] = name
    new_info['number'] = number
    new_info["date"] = get_date()
    new_info["created"] = round(time.time())
    new_info["address"] = "浙江省杭州市西湖区"
    new_info["area"] = "浙江省 杭州市 西湖区"
    new_info["province"] = new_info["area"].split(' ')[0]
    new_info["city"] = new_info["area"].split(' ')[1]
    new_info['jrdqtlqk[]'] = 0
    new_info['jrdqjcqk[]'] = 0
    new_info['sfsqhzjkk'] = 1
    new_info['sqhzjkkys'] = 1
    new_info['sfqrxxss'] = 1
    new_info['jcqzrq'] = ""
    new_info['gwszdd'] = ""
    new_info['szgjcs'] = ""

    Forms = new_info
    Forms['verifyCode'] = get_code(session, headers)

    # 获取回应
    respon = session.post(url_save, data=Forms, headers=headers).content
    print(respon.decode())



deal_person1()
