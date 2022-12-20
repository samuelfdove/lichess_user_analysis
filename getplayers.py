import chess
import chess.pgn
import os


os.chdir(r'C:\Users\samue\Documents\sideproj\gamedataanalysis')

pgns = open("lichess_db_standard_rated_2015-06.pgn",'r')
#pgns = open("test.pgn",'r')
lopfile = open('listofplayers.txt','w')
lop = []
#hello//////////////////

game = chess.pgn.read_game(pgns)
i = 0
j = 0

while game != None:
#while j < 10000:
    if i%10000==0:
        print(i,j)
    whitep = game.headers["White"]
    blackp = game.headers["Black"]

    for line in lop:
        if line == whitep:
            whitep = ""
        if line==blackp:
            blackp = ""

    if whitep != "":
        lop.append(whitep)
        j+=1

    if blackp != "":
        lop.append(blackp)
        j+=1

    game = chess.pgn.read_game(pgns)
    i +=1

for i in range(len(lop)):
    print(lop[i],file = lopfile)

