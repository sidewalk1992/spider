#!/usr/bin/env python
#coding=utf-8

import requests
import re
import os
import os.path
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class WeiboSpider():
    def __init__(self, url_info):
        self.cookie = {"Cookie":"_T_WM=e26f397cdb0cec732425070d63e89adf; gsid_CTandWM=4uLmCpOz5kJLELSPcC0q7733d3y; ALF=1469609186; SUB=_2A256dJjYDeTxGedI41IR8inOyTyIHXVZljiQrDV6PUJbktBeLUKlkW1gl0PjZ8gdvkvBPXWaz0QBaVasrw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFSVMGIDOQjd8MW-FxPhgy75JpX5o2p5NHD95QpSon7ehzNeoz7Ws4DqcjePfvKIgxLUc8jIfvk; SUHB=0JvhH0Zj4Q8H6X; SSOLoginState=1467017352"}
        self.name = url_info['name']
        self.homeUrl = url_info['url']
        self.images = []
        if not os.path.exists('./weibo_images'):
            os.mkdir('./weibo_images')
        if not os.path.exists('./weibo_images/'+self.name):
            os.mkdir('./weibo_images/'+self.name)

    def __load_page(self, pageNo):
        """加载html页面"""
        url = self.homeUrl + '?page=' + str(pageNo)
        return requests.get(url=url, cookies=self.cookie).content 

    def __process_data(self, htmlPage):
        """ 从html页面中提取图片的信息 """
        pic_url = re.findall(r'http://ww.\.sinaimg.cn/wap180/\w+.\w{3,4}', htmlPage)
        for url in pic_url:
            url = url.replace('wap180', 'large')
            info = {}
            info['name'] = re.findall(r'\w{32}.\w{3,4}', url)[0]
            info['url'] = url
            self.images.append(info)

    def __save_image(self, imageName, content):
        """ 保存图片 """
        print imageName
        with open(imageName, 'wb') as fp:
            fp.write(content)

    def get_image_info(self, page=1):
        """ 得到图片信息 """
        for i in range(page):
            self.__process_data(self.__load_page(i+1))

    def down_images(self):
        """ 下载图片 """
        print "{} images will be download".format(len(self.images))
        for key, image in enumerate(self.images):
            print 'download {0} ...'.format(key+1)
            try:
                req = requests.get(image["url"])
            except :
                print 'error'
            imageName = os.path.join("./weibo_images/" + self.name + '/', image["name"])
            self.__save_image(imageName, req.content)

if __name__ == '__main__':
    urls_info = [
        #{"name":u"鹿晗", "url":"http://weibo.cn/u/5238700136"},
        #{"name":u"吴亦凡", "url":"http://weibo.cn/u/5129183523"}, 
        {"name":"Bigbang", "url":"http://weibo.cn/iloveyjs"},
        {"name":u"李易峰", "url":"http://weibo.cn/onlyforliyifeng"}, 
        {"name":"EXO", "url":"http://weibo.cn/u/3829735245"}, 
        {"name":u"少女时代", "url":"http://weibo.cn/ttian0731"}, 
        {"name":u"防弹少年团", "url":"http://weibo.cn/u/2418754967"}
    ]

    print '\n************************开始爬虫************************'
    for url_info in urls_info:
        spider = WeiboSpider(url_info)
        spider.get_image_info(100)
        spider.down_images()
    print '************************爬虫完成************************\n'