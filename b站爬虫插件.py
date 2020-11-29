import requests
import re
import random


class BLBL(object):
    def __init__(self, url, cookie, referer):
        # 需要爬取的网页前缀 例如:https://www.bilibili.com/video/av49035382       ?from=search&seid=1058195128616882249
        self.base_url = url
        # cookie内容
        self.cookie = cookie
        # referer内容
        self.referer = referer
        # 请求头信息
        self.accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        self.accept_Encoding = 'gzip, deflate, br'
        self.accept_Language = 'zh-CN,zh;q=0.9,en;q=0.8'
        self.user_agent = "User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) "

    def html(self):
        # 访问起始网页需添加的请求头，不加的话，得不到完整的源代码（反爬）
        base_headers = {
            'Accept': self.accept,
            'Accept-Encoding': self.accept_Encoding,
            'Accept-Language': self.accept_Language,
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': self.cookie,
            'Host': 'www.bilibili.com',
            'Referer': self.referer,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.user_agent
        }
        # 请求网页
        base_response = requests.get(self.base_url, headers=base_headers)
        print(base_headers)
        # 获取网页html代码
        html = base_response.text
        # print(html.headers)
        return html

    def xin_xi(self, html):
        print(html)
        try:
            # 获取视频名称
            video_name = re.search('<title>(.+)</title>', html, re.S).group(1) + '.flv'
        except:
            # 如果获取失败,就随机一个名字
            video_name = str(random.randint(100000,1000000))+'.flv'
        print(video_name)
        # 获取视频链接
        download_url = re.search(r'("url":"|"baseUrl":"|"backupUrl":\[")(.+?)("|"])', html, re.S).group(2)
        print(download_url,111)
        # 获取主机信息
        host = re.search(r'//(.+\.com)', download_url, re.S).group(1)
        print(host)
        return video_name, download_url, host

    def video(self, html):
        # 获取视频名称,视频网址,主机
        video_name, download_url, host = self.xin_xi(html)
        # 请求视频下载地址时需要添加的请求头
        download_headers = {
            'User-Agent': self.user_agent,
            'Referer': self.referer,
            'Origin': 'https://www.bilibili.com',
            'Host': host,
            'Accept': self.accept,
            'Accept-Encoding': self.accept_Encoding,
            'Accept-Language': self.accept_Language
        }
        a = ['1.195.11.157:21158',
            '121.20.53.252:15060',
            '125.111.118.224:19365',
            '121.230.211.50:18537',
            '106.226.239.28:20426',
            '106.9.171.20:20621',
            '220.248.157.204:18528',
            '117.81.173.226:17273',
            '171.12.176.88:21839',
            '125.105.49.23:20986'
             ]
        proxies = {'http':a[random.randint(0,len(a)-1)],
                   "https":a[random.randint(0,len(a)-1)]}
        # 获取视频资源,并写入文件
        with open(video_name, 'wb') as f:
            f.write(requests.get(download_url, headers=download_headers, stream=True, verify=False).content)

    def run(self):
        html = self.html()
        self.video(html)
        print('爬取成功')


if __name__ == '__main__':
    url=input("请输入网址:")
    cookie = ""
    referer = "https://www.bilibili.com/video/BV1KZ4y1j7rP?spm_id_from=333.851.b_7265706f7274466972737432.8"
    blbl = BLBL(url, cookie, referer)
    blbl.run()