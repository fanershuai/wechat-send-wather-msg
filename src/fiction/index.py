import requests
from bs4 import BeautifulSoup
import os

from src.fiction.model.fiction import Fiction

path = 'fiction/txt'
domain = "https://www.meiwen.com.cn"
listUrl = '/juzi/zheli/%s.html'
listFiction = []


def getBf(url):
    resp = requests.get(url)
    bf = BeautifulSoup(resp.text, features="lxml")
    return bf


def getPageNo(url):
    pageTxt = getBf(url).find('div', class_='page')
    lis = pageTxt.find_all('li')
    liLast = lis[len(lis) - 1]
    return int(liLast.strong.string)


def startload(url):
    bf = getBf(url)
    body = bf.find("ul", class_='tbody')
    alist = body.findAll('a', class_='meiwen')
    for i in range(len(alist)):
        print(alist[i].string + '___' + alist[i].attrs['href'])

        # fiction = Fiction(alist[i].string, domain + alist[i].attrs['href'], "")
        # listFiction.append(fiction)
        getContent(domain + alist[i].attrs['href'], alist[i].string)


def getContent(url, title):
    content = ""
    bf = getBf(url)
    contentbf = bf.find('div', class_='content')
    txts = contentbf.findAll('p')
    for i in range(len(txts)):
        if not txts[i] == '':
            content = content + txts[i].text.replace('<br/>','\n\n')+'\n'
    writer(title, content,url)


def writer(name, txt,url):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+ '/'+name+".txt", 'w', encoding='utf-8') as f:
        f.write(name + '\n\n')
        f.write(url+'\n\n')
        f.writelines(txt)
        f.flush()


if __name__ == '__main__':
    # 获取总页数
    pageNo = getPageNo(domain + listUrl % 1)

    for i in range(1, pageNo + 1):
        startload(domain + listUrl % i)

    # 开始请求内容
