import requests
import json
import sqlite3
import os
import time
import chess
import chess.pgn
import io

db = sqlite3.connect("players3_14.db")
a = db.execute("SELECT userID FROM perfs JOIN users ON users.ID=perfs.userID WHERE rating<800 AND gametype='rapid' AND seen_time>1634113750")
db2 = sqlite3.connect("playersjert4.db")
db2.execute("DROP TABLE ply")
db2.execute("CREATE TABLE ply (ID INTEGER PRIMARY KEY AUTOINCREMENT, name char(30) UNIQUE, rating INT,isonline INT);")

players = []

for row in a:
	players.append(row[0])
	db2.execute("INSERT INTO ply (name) VALUES ('"+row[0]+"');")
	

db2.commit()
i = 1
a = db2.execute("SELECT name FROM ply WHERE ID = "+str(i)+" ORDER BY ID;")
while 1==1:
    player = ""
    for row in a:
        player = row[0]
        print(player)
    rr = requests.get('https://lichess.org/api/games/user/'+player+'?since=1652430550&max=20&rated=true&perfType="rapid"&moves=0')
    while rr.status_code == 429:
        print('sleeping')
        time.sleep(605)
        rr = requests.get('https://lichess.org/api/games/user/'+player+'?since=1652430550&max=20&rated=true&perfType="rapid"&moves=0')

    pgntext = io.StringIO(rr.text)
    game = chess.pgn.read_game(pgntext)

    while game != None:
        whitep = game.headers["White"]
        blackp = game.headers["Black"]
        islowrated = 1
        if whitep==player:
            p = blackp
            pelo = game.headers["BlackElo"]
        else:
            p = whitep
            pelo = game.headers["WhiteElo"]
        if int(pelo)<900:
            try:
                db2.execute("INSERT INTO ply (name,rating) VALUES ('"+p+"',"+pelo+");")
            except:
                pass
        game = chess.pgn.read_game(pgntext)
    db2.commit()
    i+=1
    a = db2.execute("SELECT name FROM ply WHERE ID = "+str(i)+" ORDER BY ID;")
