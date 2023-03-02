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


def get_weather_now():
  url = "https://devapi.qweather.com/v7/weather/now?location=101030100&key=afc9647291ad4e3e993aa97899b177d7"
  res = requests.get(url).json()
  weather = res['now']
  return weather['text'], int(weather['temp']), int(weather['feelsLike']), int(weather['windDir']),int(weather['windScale']),weather['humidity']+'%','优'

def get_weather_today():
  url = "https://devapi.qweather.com/v7/weather/3d?location=101030100&key=afc9647291ad4e3e993aa97899b177d7"
  res = requests.get(url).json()
  weather2 = res['daily'][0]
  return weather2['textDay'], int(weather['temp']), int(weather['tempMin']), int(weather['tempMax']),int(weather['humidity']),weather['windDirDay'],'优'

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
weatherText, temperature, low,wind ,high, humidity,air   = get_weather_now()
text, author = get_words2()

data = {"weather":{"value":weatherText},"temperature":{"value":temperature,"color": "#FF0000" if temperature >= 35 else "#FF9900" if 30<=temperature<35 else "#00FF00" if  15<=temperature<30 else "#00BFFF" if temperature<15 else "#0000CD"},"low":{"value":low,"color": "#FF0000" if low >= 35 else "#FF9900" if 30<=low<35 else "#00FF00" if  15<=low<30 else "#00BFFF" if low<15 else "#0000CD"},"high":{"value":high,"color": "#FF0000" if high >= 35 else "#FF9900" if 30<=high<35 else "#00FF00" if  15<=high<30 else "#00BFFF" if high<15 else "#0000CD"},"humidity":{"value":humidity},"wind":{"value":wind},"air":{"value":air,"color":"#00FF00" if air=="优" else "#FF9900" if air=="良" else "#FF0000" },"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words()+" ", "color":get_random_color()},"words2":{"value":text+' —— '+ author+"  ", "color":get_random_color2()}}
res = wm.send_template(user_id, template_id, data)
print(res)
