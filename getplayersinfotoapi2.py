import requests
import json
import sqlite3
import os
import time

os.chdir("C:/Users/samue/Documents/sideproj/gamedataanalysis")
players = open('listofplayers.txt','r')

db = sqlite3.connect("players3_14.db")
#
db.execute("DROP TABLE users")
db.execute("DROP TABLE perfs")
db.execute("DROP TABLE count")
db.execute("CREATE TABLE users (ID char(30) PRIMARY KEY,username char(30),created_time INT,seen_time INT,playtime INT,completionRate INT, gamenum INT);")
db.execute("CREATE TABLE perfs (perfsID INTEGER PRIMARY KEY AUTOINCREMENT, userID char(30), gametype CHAR(30), games INT,rating INT, rd INT, prog INT)")
db.execute("CREATE TABLE count (countID INTEGER PRIMARY KEY AUTOINCREMENT, userID char(30), alll INT, rated INT,ai INT,draw INT,drawH INT,loss INT,lossH INT,win INT,winH INT,bookmark INT, playing INT,important INT,me INT)")

numers = 0

for i in range(189):#189
    playblock = ''
    playblock += (players.readline().strip())
    for j in range(299):
        playblock += (','+players.readline().strip())
    #print(playblock)
    rr = requests.post('https://lichess.org/api/users',data=playblock)
    while rr.status_code == 429:
        print('sleeping')
        time.sleep(605)
        rr = requests.post('https://lichess.org/api/users',data=playblock)

    l = len(rr.json())
    for j in range(l):
        r = rr.json()[j]

        try:

            try:
                db.execute("INSERT INTO users (ID, username,created_time,seen_time,playtime,completionRate,gamenum) VALUES ('"+str(r["id"])+"','"+str(r["username"])+"',"+str(round(r["createdAt"]/1000))+","+str(round(r["seenAt"]/1000))+","+str(r["playTime"]["total"])+","+"0"+","+str(j)+")")
            except:
                db.execute("INSERT INTO users (ID, username,created_time,seen_time,playtime,completionRate,gamenum) VALUES ('"+str(r["id"])+"','"+str(r["username"])+"',"+str(round(r["createdAt"]/1000))+","+str(round(r["seenAt"]/1000))+","+"NULL"+","+"0"+","+str(j)+")")

            db.execute("INSERT INTO perfs (userId,gametype,games,rating,rd,prog) VALUES ('"+str(r["id"])+"','blitz',"+str(r["perfs"]["blitz"]["games"])+","+str(r["perfs"]["blitz"]["rating"])+","+str(r["perfs"]["blitz"]["rd"])+","+str(r["perfs"]["blitz"]["games"])+")")
            db.execute("INSERT INTO perfs (userId,gametype,games,rating,rd,prog) VALUES ('"+str(r["id"])+"','bullet',"+str(r["perfs"]["bullet"]["games"])+","+str(r["perfs"]["bullet"]["rating"])+","+str(r["perfs"]["bullet"]["rd"])+","+str(r["perfs"]["bullet"]["games"])+")")
            db.execute("INSERT INTO perfs (userId,gametype,games,rating,rd,prog) VALUES ('"+str(r["id"])+"','correspondence',"+str(r["perfs"]["correspondence"]["games"])+","+str(r["perfs"]["correspondence"]["rating"])+","+str(r["perfs"]["correspondence"]["rd"])+","+str(r["perfs"]["correspondence"]["games"])+")")
            db.execute("INSERT INTO perfs (userId,gametype,games,rating,rd,prog) VALUES ('"+str(r["id"])+"','classical',"+str(r["perfs"]["classical"]["games"])+","+str(r["perfs"]["classical"]["rating"])+","+str(r["perfs"]["classical"]["rd"])+","+str(r["perfs"]["classical"]["games"])+")")
            db.execute("INSERT INTO perfs (userId,gametype,games,rating,rd,prog) VALUES ('"+str(r["id"])+"','rapid',"+str(r["perfs"]["rapid"]["games"])+","+str(r["perfs"]["rapid"]["rating"])+","+str(r["perfs"]["rapid"]["rd"])+","+str(r["perfs"]["rapid"]["games"])+")")
            try:
                 db.execute("INSERT INTO perfs (userId,gametype,games,rating,rd,prog) VALUES ('"+str(r["id"])+"','puzzle',"+str(r["perfs"]["puzzle"]["games"])+","+str(r["perfs"]["puzzle"]["rating"])+","+str(r["perfs"]["puzzle"]["rd"])+","+str(r["perfs"]["puzzle"]["games"])+")")
            except:
                
                pass
            
            try:
                db.execute("INSERT INTO count (userID,alll,rated,ai,draw,drawH,loss,lossH,win,winH,bookmark,playing,important,me) VALUES ('"+r["id"]+"','"+str(r["count"]["all"])+"','"+str(r["count"]["rated"])+"','"+str(r["count"]["ai"])+"','"+str(r["count"]["draw"])+"','"+str(r["count"]["drawH"])+"','"+str(r["count"]["loss"])+"','"+str(r["count"]["lossH"])+"','"+str(r["count"]["win"])+"','"+str(r["count"]["winH"])+"','"+str(r["count"]["bookmark"])+"','"+str(r["count"]["playing"])+"','"+str(r["count"]["import"])+"','"+str(r["count"]["me"])+"')")
                print('here')
            except Exception as e:
                pass
            #db.execute("INSERT INTO testtable (ID, name) VALUES (1,'hhey')")
            db.commit()
        except Exception as e:

            numers += 1
            #print(e)
            #print(r)
            #print('-----------')
            pass 
    print(i,'-',i*300)
    
print(numers)

    