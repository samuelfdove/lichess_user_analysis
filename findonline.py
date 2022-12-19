import requests
import json
import sqlite3
import os
import time
import chess
import chess.pgn
import io

db = sqlite3.connect("playersjert3.db")

a = db.execute("SELECT name FROM ply ORDER BY isonline DESC;")
db.execute("UPDATE ply SET isonline=NULL")
db.commit()
allplayers = [[]]
i = 0
for row in a:
    allplayers[i].append(row[0])
    if len(allplayers[i])==100:
        allplayers.append([])
        i+=1

onlinestatus = []



for i in range(len(allplayers)):
    rr = requests.get('https://lichess.org/api/users/status?ids='+",".join(allplayers[i]))
    currplay = rr.json()
    for j in range(len(currplay)):
        if 'playing' in (currplay[j].keys()):
            db.execute("UPDATE ply SET isonline=1 WHERE name = '"+currplay[j]['name']+"';")
        else:
            db.execute("UPDATE ply SET isonline=0 WHERE name = '"+currplay[j]['name']+"';")
    db.commit()
    
