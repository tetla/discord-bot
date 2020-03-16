# discord-bot
discord用のボットです

## 起動方法

通常の起動方法（SSH閉じたらスクリプト止まる）
``` python
python3 discord-bot.py
```

ログアウト後も動かす方法
``` python
nohup python3 discord-bot.py > out.log &
```

## その他のコマンド

プロセスの探し方
``` python
ps aux | grep discord-bot.py | grep -v grep | awk '{ print "kill -9", $2 }' | sh
# もしくはこっち(若干乱暴)
pkill python3
```
