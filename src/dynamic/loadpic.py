import requests
from bs4 import BeautifulSoup as bs
import os
import re

#uid即进入对方微博主页后网址部分/u/后的那一串数字
uid = '3276317104'
url = 'https://weibo.cn/u/' + uid
cookie = 'SINAGLOBAL=112.20.116.21_1561261033.162011; UOR=www.google.com,blog.sina.com.cn,; ULV=1561284932496:1:1:1::; U_TRS1=00000044.fe3a1647.5d0f5144.a47fb52c; SCF=AtuELV0nq7wfLpQzdy1hi7Gn2ZHyzVNl1HWqtmLx_kQBDsqRvjhA7JqGynDX3N7vM-QYoO6d_9Pin9u_Xl0kD-s.; SUB=_2AkMqfUdkf8NxqwJRmPAcxW3hao9_ywnEieKcIba_JRMyHRl-yD9jqnQ9tRB6Af1piylNcEIA3WQUkAQDS4djA7r9PBiU; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWqEBBsAnRlA6HZKnsvGCPd; Apache=121.224.111.248_1562833300.338958'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', 'Cookie': cookie}

r = requests.get(url, headers=headers,verify=False)
soup = bs(r.text, 'html.parser')
# 所访问的微博用户名
weibo_user_name = soup.find('title').text.replace('的微博', '')
# 存放图片的根目录
rootDir = '/微博配图相册/' + weibo_user_name + '/'
# 微博总页数,通过审查元素可知
totalPage = int(soup.find('input', attrs={'name': 'mp'}).attrs['value'])
print('总共检测到%d页微博页面' % totalPage)
# 每页微博的URL的列表
weibo_urlList = [url + '?page=' + str(i + 1) for i in range(totalPage)]
#当前已爬取的图片总数
pictrue_num = 0
for page, weibo_url in enumerate(weibo_urlList):
    r = requests.get(weibo_url, headers=headers)
    soup = bs(r.text, 'html.parser')
    #每条微博所对应的标签代码块列表
    weibo_tags_list = soup.find_all('div', attrs={'class': 'c'}, id=True)
    #微博发送时间与微博配图的字典
    imgs_urls_dic = {}
    for entry, weibo_tag in enumerate(weibo_tags_list):
        print('正在爬取第%d页第%d条微博' % (page + 1, entry + 1))
        #获取微博发送时间
        hms = ' '.join(weibo_tag.find(
            'span', attrs={'class': 'ct'}).text.replace('\xa0', ' ').replace(':', '-').split(' ')[:2])
        #该条微博若带有组图，获取组图中所有图片的URL
        if weibo_tag.find('a', text=re.compile('组图')):
            imgs_url = weibo_tag.find('a', text=re.compile('组图')).attrs['href']
            html = requests.get(imgs_url, headers=headers)
            imgs_soup = bs(html.text, 'html.parser')
            imgs_tags_List = imgs_soup.find_all('img', alt='图片加载中...')
            img_urls_list = [imgs_tag.attrs['src'].replace(
                'thumb180', 'large') for imgs_tag in imgs_tags_List]
            imgs_urls_dic[hms] = img_urls_list
        #该条微博仅有一张配图，或者没有图片，获取图片的URL
        else:
            img_tags_List = weibo_tag.find_all('img', alt='图片')
            img_urls_list = [img_tag.attrs['src'].replace(
                'wap180', 'large') for img_tag in img_tags_List]
            imgs_urls_dic[hms] = img_urls_list
    print('第%d页微博爬取完毕,开始生成图片' % (page + 1))
    for hms, img_urls_list in imgs_urls_dic.items():
        for index, img_url in enumerate(img_urls_list):
            #生成图片的存放路径，图片被命名为微博发送时间
            path = rootDir + hms
            #如果一条微博在同一时间发送了多张图片(即组图)的命名处理
            if(index > 0):
                path = path + '(' + str(index) + ')'
            path = path + '.jpg'
            try:
                if not os.path.exists(rootDir):
                    #makedirs递归生成多级目录，mkdir仅能生成一级目录
                    os.makedirs(rootDir)
                if not os.path.exists(path):
                    r = requests.get(img_url)
                    with open(path, 'wb') as f:
                        f.write(r.content)
                        pictrue_num = pictrue_num + 1
                        print('success,成功爬取第%d张图片' % pictrue_num)
                else:
                    print('%s已经存在' % path)
            except:
                print('爬取失败,%s' % img_url)
print('总共爬取了%d张图片，存放在 %s 目录下' % (pictrue_num, rootDir))
