from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high']),weather['humidity'],weather['wind'],weather['airQuality']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_words2():
  words2 = requests.get("https://saying.api.azwcl.com/saying/get")
  if words2.status_code != 200:
    return get_words2()
  return words2.json()['data']['content'],words2.json()['data']['author']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_random_color2():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, low, high, humidity, wind, air  = get_weather()
word = get_words()
text, author = get_words2()

data = {"weather":{"value":wea},"temperature":{"value":temperature,"color": "#FF0000" if temperature > 30 else "#00FF00"},"low":{"value":low+"  ","color": "#FF0000" if low > 30 else "#00FF00"},"high":{"value":high,"color": "#FF0000" if high > 30 else "#00FF00"},"humidity":{"value":humidity},"wind":{"value":wind},"air":{"value":air,"color":"#00FF00" if air=="优" else "#FF9900" },"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":word+" ", "color":get_random_color()},"words2":{"value":text+' —— '+ author+"    ", "color":get_random_color2()}}
res = wm.send_template(user_id, template_id, data)
print(res)
