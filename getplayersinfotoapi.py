import requests
import json
import sqlite3
import os
import chess
import chess.pgn

os.chdir("C:/Users/samue/Documents/sideproj/gamedataanalysis")


db = sqlite3.connect("test.db")
#db.execute("DROP TABLE users")
#db.execute("DROP TABLE perfs")
#db.execute("DROP TABLE count")
#db.execute("CREATE TABLE users (ID char(30) PRIMARY KEY,username char(30),created_time INT,seen_time INT,playtime INT,completionRate INT, gamenum INT);")
#db.execute("CREATE TABLE perfs (perfsID INTEGER PRIMARY KEY AUTOINCREMENT, userID char(30), gametype CHAR(30), games INT,rating INT, rd INT, prog INT)")
#db.execute("CREATE TABLE count (countID INTEGER PRIMARY KEY AUTOINCREMENT, userID char(30), alll INT, rated INT,ai INT,draw INT,drawH INT,loss INT,lossH INT,win INT,winH INT,bookmark INT, playing INT,important INT,me INT)")
pgns = open("lichess_db_standard_rated_2015-06.pgn",'r')


i = 0
j = 0

game = chess.pgn.read_game(pgns)

while game != None:
    if j%1000==0:
        print(j)
    if i%100==0:
        print("ERRORS:",i)
    game = chess.pgn.read_game(pgns)
    whitep = game.headers["White"]
    blackp = game.headers["Black"]
    players = [whitep,blackp]
    for k in range(2):
        play = players[k]
        pstring = "https://lichess.org/api/user/"+play
        #print(play)
        try:
            r = requests.get(pstring)
            #print(r.text)
            db.execute("INSERT INTO users (ID, username,created_time,seen_time,playtime,completionRate,gamenum) VALUES ('"+str(r.json()["id"])+"','"+str(r.json()["username"])+"',"+str(round(r.json()["createdAt"]/1000))+","+str(round(r.json()["seenAt"]/1000))+","+str(r.json()["playTime"]["total"])+","+"0"+","+str(j)+")")

            db.execute("INSERT INTO perfs (userId,gametype,games,rating,rd,prog) VALUES ('"+str(r.json()["id"])+"','blitz',"+str(r.json()["perfs"]["blitz"]["games"])+","+str(r.json()["perfs"]["blitz"]["rating"])+","+str(r.json()["perfs"]["blitz"]["rd"])+","+str(r.json()["perfs"]["blitz"]["games"])+")")
            db.execute("INSERT INTO perfs (userId,gametype,games,rating,rd,prog) VALUES ('"+str(r.json()["id"])+"','puzzle',"+str(r.json()["perfs"]["puzzle"]["games"])+","+str(r.json()["perfs"]["puzzle"]["rating"])+","+str(r.json()["perfs"]["puzzle"]["rd"])+","+str(r.json()["perfs"]["puzzle"]["games"])+")")
            db.execute("INSERT INTO perfs (userId,gametype,games,rating,rd,prog) VALUES ('"+str(r.json()["id"])+"','bullet',"+str(r.json()["perfs"]["bullet"]["games"])+","+str(r.json()["perfs"]["bullet"]["rating"])+","+str(r.json()["perfs"]["bullet"]["rd"])+","+str(r.json()["perfs"]["bullet"]["games"])+")")
            db.execute("INSERT INTO perfs (userId,gametype,games,rating,rd,prog) VALUES ('"+str(r.json()["id"])+"','correspondence',"+str(r.json()["perfs"]["correspondence"]["games"])+","+str(r.json()["perfs"]["correspondence"]["rating"])+","+str(r.json()["perfs"]["correspondence"]["rd"])+","+str(r.json()["perfs"]["correspondence"]["games"])+")")
            db.execute("INSERT INTO perfs (userId,gametype,games,rating,rd,prog) VALUES ('"+str(r.json()["id"])+"','classical',"+str(r.json()["perfs"]["classical"]["games"])+","+str(r.json()["perfs"]["classical"]["rating"])+","+str(r.json()["perfs"]["classical"]["rd"])+","+str(r.json()["perfs"]["classical"]["games"])+")")
            db.execute("INSERT INTO perfs (userId,gametype,games,rating,rd,prog) VALUES ('"+str(r.json()["id"])+"','rapid',"+str(r.json()["perfs"]["rapid"]["games"])+","+str(r.json()["perfs"]["rapid"]["rating"])+","+str(r.json()["perfs"]["rapid"]["rd"])+","+str(r.json()["perfs"]["rapid"]["games"])+")")

            db.execute("INSERT INTO count (userID,alll,rated,ai,draw,drawH,loss,lossH,win,winH,bookmark,playing,important,me) VALUES ('"+r.json()["id"]+"','"+str(r.json()["count"]["all"])+"','"+str(r.json()["count"]["rated"])+"','"+str(r.json()["count"]["ai"])+"','"+str(r.json()["count"]["draw"])+"','"+str(r.json()["count"]["drawH"])+"','"+str(r.json()["count"]["loss"])+"','"+str(r.json()["count"]["lossH"])+"','"+str(r.json()["count"]["win"])+"','"+str(r.json()["count"]["winH"])+"','"+str(r.json()["count"]["bookmark"])+"','"+str(r.json()["count"]["playing"])+"','"+str(r.json()["count"]["import"])+"','"+str(r.json()["count"]["me"])+"')")
            #db.execute("INSERT INTO testtable (ID, name) VALUES (1,'hhey')")
            db.commit()
        except Exception as e:
            i+=1
            print(e)
            print(r.text)
            print('-----------')
            pass
            #print(e)
    j+=1

    if j<100:
        print(players)

print(j)