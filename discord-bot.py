import os
import subprocess
import discord
from discord.ext import tasks
from datetime import datetime
import requests
import random
from dotenv import load_dotenv
from tinydb import TinyDB, Query

import markov

load_dotenv()

db = TinyDB('db.json')

client = discord.Client()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
SERVICE_ACCOUNT_ID = os.environ["SERVICE_ACCOUNT_ID"]
PROJECT_NAME = os.environ["PROJECT_NAME"]
INSTANCE_ZONE = os.environ["INSTANCE_ZONE"]
INSTANCE_NAME = os.environ["INSTANCE_NAME"]

# load markov model
with open('model/maekawa_serif.json') as f:
    markov_json = f.read()

@client.event
async def on_ready():
    print("起動したにゃ")
    # Gitのハッシュ値を確認する。
    # hash_val = get_hash()
    # channel = client.get_channel(689851923414646913) # みくちゃんのお部屋のID
    # await channel.send('起動完了！ 現在のバージョンは %s にゃ' % hash_val)

@client.event
async def on_message(message):
    """
    Usage: /minecraft [start|stop|status|]
    ---
    start:
        サーバを開始する
    stop:
        サーバを停止する
    status:
        サーバのステータスを確認する
    """
    if message.content.startswith('/minecraft'):
        command = message.content.split(' ')[1]
        if command == 'start':
            await message.channel.send('サーバを起動してるよ...')
            start_server()
            await message.channel.send('サーバが起動したよ！')
        elif command == 'stop':
            await message.channel.send('サーバを停止してるよ...')
            stop_server()
            await message.channel.send('サーバを停止したよ！')
        elif command == 'status':
            status = describe_server()
            if 'RUNNING' in status:
                await message.channel.send('サーバは動いてるにゃ')
            elif 'STOPPING' in status:
                await message.channel.send('サーバを止めてるとこだから焦るにゃ')
            elif 'TERMINATED' in status:
                await message.channel.send('サーバは止まってるにゃ')
            elif 'STOPPED' in status:
                await message.channel.send('サーバは止まってるにゃ')
            else:
                await message.channel.send('わからないにゃ～')

    # [TODO]肥大化してきたら分割する。
    if message.content == '/miku':
        await message.channel.send('にゃーん')
    
    if message.content == '/mikunyan':
        await message.channel.send('なぁに%sチャン' % message.author.name)

    if message.content == '/riina':
        await message.channel.send('りーなチャン！？')

    if message.content == '/nero':
        await message.channel.send('早く寝るにゃ')

    if message.content == '/neet':
        await message.channel.send('それもまたアイカツにゃ')

    if message.content == '/ruta':
        ruta_message = "【特装版は5/8(金)まで！】Funky Dancing!公演を振り返るBlu-rayが遂に映像化！"
        ruta_url = "https://shop.asobistore.jp/products/detail/149935-00-00-t_as_sp"
        await message.channel.send('<@618849773906165770> ' + ruta_message)
        await message.channel.send('<@618849773906165770> ' + ruta_url)
    
    if message.content == '/tokyo':
        today, tomorrow = get_weather('130010') # 東京は 130010
        await message.channel.send('%s' % today)
        await message.channel.send('%s にゃ' % tomorrow)
    
    if message.content == '/omikuji':
        fortune = pull_omikuji()
        await message.channel.send('%sチャンの今日の運勢は%sにゃ' % (message.author.name, fortune))

    if message.content == '/nana':
        await message.channel.send('ミミミン！ミミミン！ウーサミン！')

    if message.content == '/kagawa':
        await message.channel.send('ゲームは1日1時間までにゃ')
    
    if message.content == '/talk':
        sentence = markov.make_sentences(markov_json)
        await message.channel.send(sentence)
    
    if message.content == '/hash':
        hash_val = get_hash()
        await message.channel.send(hash_val)
    
    if message.content == '/remaind':
        hoge = remainder(message)
        await message.channel.send(hoge)


# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    if now == '15:00': # 日本時間 00:00
        channel = client.get_channel(689851923414646913) # みくちゃんのお部屋のID
        await channel.send('こんな時間までゲームしてるの？Pチャンすごーい！')

# サーバを開始させるメソッド
def start_server():
    command = f'/snap/bin/gcloud --account={SERVICE_ACCOUNT_ID} compute instances start {INSTANCE_NAME} --project {PROJECT_NAME} --zone {INSTANCE_ZONE}'
    subprocess.call(command.split())
    return

# サーバを停止させるメソッド
def stop_server():
    command = f'/snap/bin/gcloud --account={SERVICE_ACCOUNT_ID} compute instances stop {INSTANCE_NAME} --project {PROJECT_NAME} --zone {INSTANCE_ZONE}'
    subprocess.call(command.split())
    return

# サーバのステータスを確認するメソッド
def describe_server():
    command = f'/snap/bin/gcloud --account={SERVICE_ACCOUNT_ID} compute instances describe {INSTANCE_NAME} --project {PROJECT_NAME} --zone {INSTANCE_ZONE}'
    res = subprocess.run(command.split(),stdout=subprocess.PIPE)
    return res.stdout.decode("ascii")

# 東京の天気を取得するメソッド
def get_weather(city_code):
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
    payload = {'city': city_code} 
    tenki = requests.get(url, params=payload).json()
    today = tenki['forecasts'][0]['date'] + " の東京の天気は " + tenki['forecasts'][0]['telop']
    if tenki['forecasts'][0]['temperature']['max'] is not None:
        today = today + "。最高気温は" + tenki['forecasts'][0]['temperature']['max']['celsius']
    tomorrow = tenki['forecasts'][1]['date'] + " の東京の天気は " + tenki['forecasts'][1]['telop']
    if tenki['forecasts'][1]['temperature']['max'] is not None:
        tomorrow = tomorrow + "。最高気温は" + tenki['forecasts'][1]['temperature']['max']['celsius']
    return (today, tomorrow)

def pull_omikuji():
    num = random.random()
    if num < 0.01:
        fortune = "猫吉"
    elif num < 0.1:
        fortune = "大吉"
    elif num < 0.4:
        fortune = "中吉"
    elif num < 0.7:
        fortune = "小吉"
    elif num < 0.9:
        fortune = "凶"
    else:
        fortune = "大凶"
    return fortune

def get_hash():
    with open("./hash.txt", mode='r') as f:
        hash_val = f.readline()
    return hash_val.strip()

def remainder(message):
    '''
    message = /remainder add date[yyyy/MM/dd] time[hh:mm] message user
    '''
    print(message.content)
    _, command, date, time, content, user = message.content.split(' ')
    return user



# ループ処理実行
loop.start()

# Discordのクライアントを起動する
client.run(DISCORD_TOKEN)