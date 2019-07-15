import time

import requests
from sqlalchemy.sql.functions import now
from wxpy import *

from threading import Timer

from src.wather.citycode import proviceCode, cityCode, countyCode

common_url = 'http://t.weather.sojson.com/api/weather/city/101'

bot = Bot(cache_path=True)
friendList = bot.friends()
groupList = bot.groups()


def wendu(code):
    # 温度API
    if code is None:
        print('请填写城市码')
        return

    w_url = common_url + code

    response = requests.get(w_url)

    city = response.json()['cityInfo']['city']

    data = response.json()['data']

    # 接口内容

    time = "时间：" + str(data['forecast'][0]['ymd'])

    city = "城市：" + str(city)

    shidu = "湿度：" + str(data['shidu'])

    pm25 = "PM2.5：" + str(data['pm25'])

    pm10 = "PM10：" + str(data['pm10'])

    quality = "空气质量：" + str(data['quality'])

    forecast_high = "最高温度：" + str(data['forecast'][0]['high'].split()[1])

    forecast_low = "最低温度：" + str(data['forecast'][0]['low'].split()[1])
    forecast_week=   str(data['forecast'][0]['week'])
    forecast_type = "天气：" + str(data['forecast'][0]['type'])
    ganmao = '感冒提醒（指数）：' + str(data['ganmao'])
    forecast_notice =  str(data['forecast'][0]['notice'])
    tip = 'Stephen提醒您：'+forecast_notice
    nr =  city + "\n" \
         + time +"  "+forecast_week+ "\n" \
        +forecast_type+"\n" \
         + shidu + "\n" \
         + pm25 + "\n" \
         + pm10 + "\n" \
         + quality + "\n" \
         + forecast_high + "\n" \
         + forecast_low + "\n" \
         + ganmao + "\n" \
         + tip+ "\n" \
         +"祝您新的一天心情愉快！"
    print(nr)
    return nr


def get_friend_by_name(name, index):
    print(friendList.search(name)[index])
    return friendList.search(name)[index]


def get_group_by_name(name, index):
    print(groupList.search(name)[index])
    return groupList.search(name)[index]


def send_new(code, grouplist_atrr=[], friendList_atrr=[]):
    try:
        content = wendu(code)

        # 获取微信名称，注：不是备注，也不是微信号

        # 发送消息

        if grouplist_atrr is not None:
            for i in range(len(grouplist_atrr)):
                get_group_by_name(grouplist_atrr[i], 0).send(content)

        if friendList_atrr is not None:
            for i in range(len(friendList_atrr)):
                get_friend_by_name(friendList_atrr[i], 0).send(content)

        # 定时发送，86400秒（1天），发送一次



    except:

        # 自己的微信名称

        # my_friend = bot.friends().search("DB.Fan")[0]
        #
        # my_friend.send("今天发送消息失败！")

        print('发送消息失败')


def timeSend():
    t = time.localtime()
    dt = time.strftime("%H:%M", t)
    print(dt)
    if dt == '06:00':
        print('发送')
        sendAll()

    ttimer = Timer(59, timeSend)
    ttimer.start()


def sendJing():
    send_new(cityCode.SUZHOU, [], ['静宝'])


def sendAll():
    # 徐洲
    send_new(cityCode.XUZHOU, ['八兄弟', '七兄弟', '地主家的傻姑娘群'], ['侯菲', '马诚', '马欣', '马诚诚'])
    # 苏州
    send_new(cityCode.SUZHOU, ['八兄弟', '群英汇', '苏州起点羽球周三', '黑枸杞研发群'], ['静宝', '李宁', '周琦', '王平'])
    # 江阴
    send_new(cityCode.JIANGYIN, ['主赐福，蒙主恩一家人'], ['坤哥'])
    # 安吉
    send_new(cityCode.ANJI, ['八兄弟'], ['罗飞湖州', '阿廖'])
    # 嘉兴
    send_new(cityCode.JIAXING, [], ['王波', '王闯'])
    # 砀山
    send_new(countyCode.DANGSHAN, ['蒋氏家族'], [])
    # 南京
    send_new(cityCode.NANJING, ['人小组', '地主家的傻姑娘群'], ['阔比', '吕顺法'])
    # 杭州
    send_new(cityCode.HANGZHOU, [], ['Zora', '李振'])
    # 北京
    send_new(cityCode.BEIJING, [], ['范忠臣'])


if __name__ == '__main__':
    timeSend()
    # send_new(cityCode.NANJING, ['人小组', '地主家的傻姑娘群'], ['阔比', '吕顺法'])
    # 北京
    # send_new(cityCode.BEIJING, [], ['范忠臣'])
    # 江阴
    # send_new(cityCode.JIANGYIN, ['主赐福，蒙主恩一家人'], ['坤哥'])
