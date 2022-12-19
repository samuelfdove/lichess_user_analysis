import requests
import json
import sqlite3
import os
import time
import chess
import chess.pgn
import io

db = sqlite3.connect("players3_14.db")
a = db.execute("SELECT userID FROM perfs WHERE rating<900 AND gametype='rapid'")
db2 = sqlite3.connect("playersjert2.db")
db2.execute("DROP TABLE ply")
db2.execute("CREATE TABLE ply (ID INTEGER PRIMARY KEY AUTOINCREMENT, name char(30) UNIQUE, isonline INT);")

players = []

for row in a:
	players.append(row[0])
	db2.execute("INSERT INTO ply (name) VALUES ('"+row[0]+"');")
	

db2.commit()
i = 1
for player in players:
	rr = requests.get('https://lichess.org/api/games/user/'+player+'?max=20&rated=true&perfType="rapid"&moves=0')
	while rr.status_code == 429:
        print('sleeping')
        time.sleep(605)
		rr = requests.get('https://lichess.org/api/games/user/'+player+'?max=20&rated=true&perfType="rapid"&moves=0')
	
	pgntext = io.StringIO(rr.text)
	game = chess.pgn.read_game(pgntext)


	while game != None:
		whitep = game.headers["White"]
		blackp = game.headers["Black"]
		
		if whitep==player:
			p = blackp
		else:
			p = whitep
		try:
			db2.execute("INSERT INTO ply (name) VALUES ('"+p+"');")
		except:
			pass
		game = chess.pgn.read_game(pgntext)
	db2.commit()
	i+=1
	print(i)
