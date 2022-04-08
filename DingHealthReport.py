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


def get_date():
    """Get current date"""
    today = datetime.date.today()
    return "%4d%02d%02d" % (today.year, today.month, today.day)




# 解决第二个人的打卡请求
url_save = 'https://healthreport.zju.edu.cn/ncov/wap/default/save'
url_index = 'https://healthreport.zju.edu.cn/ncov/wap/default/index'

# 给出headers和cookies，令其可以免登录
# headers和cookies的确定方法为：
# 1. Chrome打开无痕页面，键入url_save网址，返回登录界面
# 2. 右键审查元素或者按F12，找到network栏
# 3. 输入账号密码并登录，然后找到“index”的“requests headers”一栏
# 4. 将cookie中的所有内容全部复制粘贴到cookies = ‘’中，用以完成请求头。
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
# cookies = 'eai-sess=a5cbru7g68sardqreor52ab0t0; UUkey=7845ce9dc936a6d37999dbca0b2153d6; _csrf=S8mwplVi9KWoF2WQ0TlCeATS6Si1PggMUPFi597fxEc=; _pv0=Zrjx4/6YuzJ3ath/vldxxLaOnhO5A20bj2PtedSBu92cvDMiQhaIA17zuZlDs2HHTWsS46uU5eM/6Yvwg+uF2642i7QQZq+cCyfC5cwYTGFPE/3fuyVIB3NyUnaaRKZoTK5HnO1k/i8iEQ6R8qsX8hanimrrrKxaikSu8Jj1iR4P8W89hxmcPE+/TSNlT0yIPIWpW/Xdxi/UQZk+exj197kAkp0JGWPav4SNhvZ/7kKebGrCnydtw8nQ19dHhIbuIQXapWEnLCCQ56yH7ik8fiM0L8Oc+Vdv/VYJD0WkjnVummjoq+6pBLhirVo+PVe+cHBhN6zSantf82WtyfB6dhk25093zwf+lq+YPrKRhu9Dr6Iv8BUCOyW/f6XiQyD2Toj1WqP8zzMGJuW9imrQWiW80fgwZ7VuTKgp9JMZSbg=; _pf0=klR3aDgwcFiknVJFRJ5KOOPRwidlBTKOWa3UqDg0XxI=; _pc0=nDHfD57vgXJDQjAw01OLDxDjyuFdg0c+aqa/4/YZ2dE=; iPlanetDirectoryPro=OHyAD7+SeUWl7JXCHo2Ppb/ba/1yNcimhNR2455jB0Nw1sDlQxZZq6XUTpGZYdqSJSAFNLTIlbLZnuuJYEr/WFxinJ58op1o81O/YXaLhz3G1CjLVU0wiqUWeO1y8NPC1Ov9IT63cm7ggIR+0ObH1fjAaSRl8C8foUMTI2CYAVtXD0mmlflVe1b4nSC3g2UVzr3hJz9qCf2KOQYrJ2SKBhxxwv0M3eamJqaaS2gznJmIgOiv2VkXZm8if4oMRxuo0jzy1yuk/mFTDVzBTCleWsvzkmSMoBxhqhd2XWa2Bnlo/DRaov1uEnJIZPZByk1ArID36A2Wnqwo47Jwb+Li65wDDQlIFvpyOGkGXB8+Epo='
cookies = 'eai-sess=ek5pqcsc0ur3hlapbtfpg13iu7; UUkey=5f19f6ec398d6ad3ae12e34203f24f3b; _csrf=S8mwplVi9KWoF2WQ0TlCeIaLjmS5q29S8Wd1fO20n2E=; _pv0=v50PHIdMmYGHSlhMPwYNFOkqcvHWjTmvNfXkBQxqOPzYJQYVVkKWoSRs53XdqRhE9xssbOqSWW3d0zJsTMZ3Af4MAbhz2aH4NgTflJW+bUw/uM3/VKAwPbbGGSuCNJWjK8AXeHZFvA9l5yym5NbC0YIlMWzbuRKafbDEPS3gf7nrKogR/LiNQ8F612UiOTKEzjd+Kc9zNYbZjPgZkvgrEzGcbI5I7hqNjlXdKikG0e5A50KEeer0j3sEh+BNzQtOEu+k8EGr31qHKrYpU0wnze3TTfx+pyn4xE+jD5c354QQWfqXT9f1kieZqLsUTDDO2ELW5/yjRtrGThge9CxKoyIO170DnSjRUnmwwgF3F3GbLOBg4l31NxmR0lYyhgTqcNwHPwa9isv3qItDUr5wEMUwJ5bIAbBTnJcWFBpD52w=; _pf0=w1p2BcfArPxAOGfggKaYcIGmBtu1ftOeln5tm5pjSDs=; _pc0=J8LKiUZMp/7DfPlEbOBbqUA92/UNRjspAL96d66e5j8Tl9AyG28jevAUVssWdFlW; iPlanetDirectoryPro=3R9w37FkG2cvRvqWsOieyufEZIqvPfaCfWRIHuafoxyOnAABUHlzKIzz0hj8Y6Vfx3dGVCNHVLBkvmTjJ08Jy1Hd0mUBv2nvNkoeS1tCdM3PELsTqnDDiBlZKQmGs8REUthiYpNbeSngN3xqVdzeRRkT455Lb4e6vGEokxa1Hz2w22MBEK7ScC4LxZvatvQ5lkps6l1cwq2oM1j4f9od/rC2EQ8Cq7zN18IqHEsunYrYiRC/qAwp/jsO8V1FBmtIgt4F4BxsEjPZEap4QN0wtpf7iG3NqPWrK8Azbr2NtyMX1Tftb7tCMl3ygQzm3yncYjGGxypdxr0XCp6x+oM7WDG8m35Uj3lHx2IWBxo5wME='
cookies_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookies.split("; ")}

# 获取session requests
session = requests.Session()

# 存储cookies信息到session中
s_cookies_stored = requests.utils.add_dict_to_cookiejar(session.cookies,cookies_dict)

r = session.get(url_index, headers = headers)
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

# 获取回应
respon = session.post(url_save, data = Forms, headers = headers).content
print(respon.decode())
