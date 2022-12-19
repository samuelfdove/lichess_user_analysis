import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt

os.chdir("C:/Users/samue/Documents/sideproj/gamedataanalysis")
db = sqlite3.connect("players1_8.db")

data =  db.execute('select * from perfs left join users on perfs.userID=users.ID')

print(data.fetchall()[0])

gametypes = ['blitz','bullet','classical','correspondence','puzzle','rapid']

selectquery = "select perfs.games,perfs.rating from perfs left join users on perfs.userID=users.ID where perfs.gametype = '"+gametypes[5]+"' and games>250"


data = db.execute(selectquery).fetchall()


x = []
y = []

for i in range(len(data)):
    x.append(data[i][0])
    y.append(data[i][1])


#plt.plot(x,y,'.')
plt.hist(y)
plt.show()
