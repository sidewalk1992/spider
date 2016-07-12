#!/usr/bin/env python
#coding=utf-8

import requests
import re
import os
import os.path
import random
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class HuabanCrawler():
    def __init__(self, name):
        self.homeUrl = 'http://huaban.com/search/?q=' + name
        self.images = []
        self.name = name
        if not os.path.exists('./images'):
            os.mkdir('./images')
        if not os.path.exists('./images/'+name):
            os.mkdir('./images/'+name)

    def __load_homePage(self):
        """ 加载主页面 """
        return requests.get(url = self.homeUrl).content

    def __make_ajax_url(self, No):
        """ 返回ajax请求的url """
        return self.homeUrl + "?i5p998kw&max=" + No + "&limit=20&wfl=1"

    def __load_more(self, maxNo):
        """ 刷新页面 """
        return requests.get(url = self.__make_ajax_url(maxNo)).content

    def __process_data(self, htmlPage):
        """ 从html页面中提取图片的信息 """
        prog = re.compile(r'app\.page\["pins"\].*')
        appPins = prog.findall(htmlPage)
        # 将js中的null定义为Python中的None
        null = None
        true = True
        if appPins == []:
            return None
        result = eval(appPins[0][19:-1])
        for i in result:
            info = {}
            info['id'] = str(i['pin_id'])
            info['url'] = "http://img.hb.aicdn.com/" + i["file"]["key"] + "_fw658"
            if 'image' == i["file"]["type"][:5]:
                info['type'] = i["file"]["type"][6:]
            else:
                info['type'] = 'NoName'
            self.images.append(info)

    def __save_image(self, imageName, content):
        """ 保存图片 """
        print imageName
        with open(imageName, 'wb') as fp:
            fp.write(content)

    def get_image_info(self, num=20):
        """ 得到图片信息 """
        self.__process_data(self.__load_homePage())
        for i in range((num-1)/20):
            self.__process_data(self.__load_more(self.images[-1]['id']))
        return self.images

    def down_images(self):
        """ 下载图片 """
        print "{} image will be download".format(len(self.images))
        for key, image in enumerate(self.images):
            print 'download {0} ...'.format(key)
            try:
                req = requests.get(image["url"])
            except :
                print 'error'
            #imageName = os.path.join("./images/" + self.name + '/', image["id"] + "." + image["type"])
            imageName = os.path.join("./images/" + self.name + '/', str(random.randint(0,99999)) + "." + image["type"])
            self.__save_image(imageName, req.content)


if __name__ == '__main__':
    stars = ['tfboys', u'鹿晗', u'吴亦凡', 'Bigbang', u'李易峰', u'杨洋', u'杨幂', 'EXO', u'少女时代', u'防弹少年团']
    for star in stars:
        print '************************开始下载'+star+'************************'
        hc = HuabanCrawler(star)
        hc.get_image_info(20)
        hc.down_images()
        print '************************下载完成'+star+'************************'
