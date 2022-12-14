from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import json
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]

heads={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0'}

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], weather['province'],weather['city'],int(weather['temp']),weather['wind'],int(weather['low']),weather['airQuality'],int(weather['high'])

# def get_count():
#   print(today)
#   delta = today - datetime.strptime(start_date, "%Y-%m-%d")
#   return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def  lizhi():
    request_url = 'https://api.vvhan.com/api/en'
    r = requests.get(request_url).json()
    print(r,"<========>")
    date = r['data']
    print(date['en'])
    return date['en']
    
def neirong():
  words = requests.get("https://api.lovelive.tools/api/SweetNothings")
  if words.status_code != 200:
    return get_words()
  return words.text
    
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, province, city,temp,wind,low ,airQuality,high= get_weather()
data = {"weather":{"value":wea,"color":get_random_color()},"province":{"value":province,"color":get_random_color()},"high":{"value":high,"color":get_random_color()},"city":{"value":city,"color":get_random_color()},"temp":{"value":temp,"color":get_random_color()},"wind":{"value":wind,"color":get_random_color()},"low":{"value":low,"color":get_random_color()},"airQuality":{"value":airQuality,"color":get_random_color()},"love_days":{"value":"999","color":get_random_color()},"birthday_left":{"value":get_birthday(),"color":get_random_color()},"words":{"value":get_words(),"color":get_random_color()},"qinghua":{"value":neirong(), "color":get_random_color()},"en":{"value":"I want to give you the best in the world, but I find that you are the best in the world", "color":get_random_color()}}
print(data)
count = 0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  count+=1

print("?????????" + str(count) + "?????????")
