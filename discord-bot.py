import os
import subprocess
import discord
from discord.ext import tasks
from datetime import datetime
import requests
import random
from dotenv import load_dotenv

import markov

load_dotenv()

client = discord.Client()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
SERVICE_ACCOUNT_ID = os.environ["SERVICE_ACCOUNT_ID"]
PROJECT_NAME = os.environ["PROJECT_NAME"]
INSTANCE_ZONE = os.environ["INSTANCE_ZONE"]
INSTANCE_NAME = os.environ["INSTANCE_NAME"]

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
    if message.content == '/help':
        mes = "以下のコマンドで話しかけてね。\n" + get_commandlist()
        await message.channel.send(mes)

    if message.content.startswith('/minecraft'):
        await message.channel.send('知責マイクラ鯖は死んだんだ\nいくら呼んでも帰っては来ないんだ\nもうあの時間は終わって、君も人生と向き合う時なんだ')

    if message.content == '/miku':
        await message.channel.send('にゃーん')
    
    if message.content == '/mikunyan':
        await message.channel.send('なぁに%sチャン' % message.author.name)
    
    if message.content == '/maekawasan':
        await message.channel.send('？？「真面目な前川があんな格好を……」')

    if message.content == '/riina':
        await message.channel.send('りーなチャン！？')

    if message.content == '/nero':
        await message.channel.send('早く寝るにゃ')

    if message.content == '/neet':
        await message.channel.send('それもまたアイカツにゃ')

    if message.content == '/ruta':
        ruta_message = "The 1998 Petrus is unquestionably a fabulous effort boasting a dense plum/purple color as well as an extraordinary nose of black fruits intermixed with caramel, mocha, and vanilla. Exceptionally pure, super-concentrated, and extremely full-bodied, with admirable underlying acidity as well as sweet tannin, it reveals a superb mid-palate in addition to the luxurious richness for which this great property is known. The finish lasts for 40-45 seconds. Patience will definitely be required. Production was 2,400 cases, about 1,600 cases less than normal. Anticipated maturity: 2008-2040"
        ruta_url = "https://www.millesimes.com/Petrus_1998_(Pomerol,_vin_rouge)"
        
        await message.channel.send('<@618849773906165770> ' + ruta_message)
        await message.channel.send('<@618849773906165770> ' + ruta_url)

    if message.content == '/petrus':
        await message.channel.send("Petrus est un vin français d’appellation d’origine contrôlée (AOC) de la région viticole de Pomerol près de Bordeaux, dont il a l'appellation. Bien que les vins de la commune de Pomerol ne fassent pas partie de la classification officielle des vins de Bordeaux, Petrus est considéré comme un des plus grands bordeaux au même titre que des grands crus classés du Médoc tels que Château Latour, Château Lafite-Rothschild, Château Mouton Rothschild, Château Margaux, ou un Pessac-Léognan du Château Haut-Brion et des vins de Saint-Émilion comme Château Angélus, Château Ausone, Château Cheval Blanc.")

    if message.content == '/goyo':
        await message.channel.send('知育菓子でも作ってろよ。')
    
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
    
    if message.content.startswith('/talk'):
        commands = message.content.split(' ')
        chara = commands[1] if len(commands) > 1 else 'miku'
        if chara == 'list':
            model_path = 'model/'
            files = os.listdir(model_path)
            model_name_list = [f.split('.')[0] for f in files if os.path.isfile(os.path.join(model_path, f))]
            await message.channel.send(f'{len(model_name_list)} 人登録されてるにゃ。')
            await message.channel.send(', '.join(model_name_list))
        else:
            try:
                with open(f'model/{chara}.json') as f:
                    markov_json = f.read()
                    sentence = markov.make_sentences(markov_json)
                    await message.channel.send(sentence)
            except Exception as e:
                print(e)
                await message.channel.send('構文が間違ってるにゃ')

# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    if now == '00:00': # 日本時間 00:00
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

def get_commandlist():
    command_list = ['/minecraft [start|stop|status]', '/help', '/talk [chara_name]','/kagawa','/nana','/omikuji','/tokyo','/goyo','/petrus','/ruta','/neet','/nero','/riina','/maekawasan','/mikunyan','/miku']
    return "\n".join(sorted(command_list))


# ループ処理実行
loop.start()

# Discordのクライアントを起動する
client.run(DISCORD_TOKEN)
