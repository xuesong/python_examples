import re
import os
import sys
from datetime import datetime, date, time

if len(sys.argv) < 2:
	print("Please use \" "+sys.argv[0]+ " logfile\" "+ " to process the log file")
	print("        all the frame processed more than 1000ms will be print out")
	print("or use \" "+sys.argv[0]+ " logfile <num>\" "+ " to process the log file")
	print("        all the frame processed more than <num> ms will be print out")
	exit()

ofilename=sys.argv[1]+"out.txt"
rfilename=sys.argv[1]+"rst.txt"

if len(sys.argv) == 3:
	priT=int(sys.argv[2])
else:
	priT=1000

###############################################################################
# get all the lines match EmptyThisBuffer and FillBufferDone
###############################################################################
fi = open(sys.argv[1],"r")
fout = open(ofilename, "w")

line = fi.readline()

while line:
	matchobj = re.search(r'OMX-VENC: EmptyThisBuffer',line)
	if matchobj:
		fout.write(line)

	else:
		matchobj = re.search(r'OMX-VENC: FillBufferDone',line)
		if matchobj:
			fout.write(line)
	line = fi.readline()
fi.close
fout.close()

fi = open(ofilename, "r")
fresult = open(rfilename, "w")


###############################################################################
# calcualte the time delta of each encode frame
###############################################################################
maxSL=100 #after find emptythisbuffer, search at most maxSL lines to find FillBufferDone, otherwise we'll treate it as an error
emptyCount = 0 # line number match emptythisbuffer
pairCount = 0	#line number match FillBufferDone and also time stamps equals emptythisbuffer TS
dList = []  		#  a list to record the delta time between encode and done


fi.seek(0,0)
line = fi.readline()
while line:
	##### find EmptyThisBuffer first
	matchobj = re.match(r'(^.{18})\s*([0-9]+)\s*([0-9]+).*OMX-VENC: EmptyThisBuffer.*timestamp ([0-9]+).*',line)
	if matchobj:
		emptyCount = emptyCount+1
		#remember the position
		position = fi.tell()
		
		feedtime = datetime.strptime(matchobj.group(1),"%m-%d %H:%M:%S.%f")
		pid=matchobj.group(2)
		tid=matchobj.group(3)
		inputTS=matchobj.group(4)
		
		##### find the FillBufferDone with same inputTS
		line = fi.readline()
		searchLine = 0
		while line:
			matchobj = re.match(r'(^.{18})\s*([0-9]+)\s*([0-9]+).*OMX-VENC: FillBufferDone.*timestamp ([0-9]+).*',line)
			if matchobj:
				doneTS = matchobj.group(4)
				if doneTS == inputTS:
					# find match ts, record delta
					donetime = datetime.strptime(matchobj.group(1),"%m-%d %H:%M:%S.%f")
					deltaT = donetime-feedtime
					dMs = int(deltaT.total_seconds()*1000)
					dList.append(dMs)
					pairCount = pairCount+1
					if dMs >= priT:
						print("encode time %d, timestamp %s" %(dMs,doneTS))
					#prepare for next search of EmptyThisBuffer
					fi.seek(position,0)
					break
			line = fi.readline()			
			#break the loop if searched more than maxSL lines
			searchLine=searchLine+1
			if (searchLine>=maxSL):
				print("********can't find done frame for TS: " + inputTS)
				break
	# return to correct file position
	line = fi.readline()

#print("empty count is:     ",emptyCount)
#print("pair is:            ",pairCount)
print("max delta time:     ", max(dList))
print("avg time:           ", sum(dList)/(len(dList)))


fi.close()
fresult.close()