import os
import subprocess
import discord
import requests
import random
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
SERVICE_ACCOUNT_ID = os.environ["SERVICE_ACCOUNT_ID"]
PROJECT_NAME = os.environ["PROJECT_NAME"]
INSTANCE_ZONE = os.environ["INSTANCE_ZONE"]
INSTANCE_NAME = os.environ["INSTANCE_NAME"]

@client.event
async def on_ready():
    print('ログイン')
    print(client.user.name)

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
        await message.channel.send('るたニキのボーナスで焼肉にゃ')
    
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




# Discordのクライアントを起動する
client.run(DISCORD_TOKEN)