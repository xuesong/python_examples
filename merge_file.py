import re
import os
import sys
from datetime import datetime, date, time

'''
import chardet
# find out what kind of encoder it used
f = open(sys.argv[2], "r")
data = f.read()
print(chardet.detect(data))
f.close()

# output {'confidence': 0.99, 'language': '', 'encoding': 'utf-8'}



'''
outf='./out.txt'

fen = open(sys.argv[1], "r")
fch = open(sys.argv[2], "r")
fou = open(outf, "w")

for i in range(1,5000):
	lien = fen.readline()
	lich = fch.readline()	
	
	fou.write(lien)
	fou.write(lich)


fen.close()
fch.close()
fou.close()


