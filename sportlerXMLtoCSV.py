#!/usr/bin/python3
import sys
from xml.dom.minidom import parse, parseString
import csv
from datetime import datetime

'''
SysArgv[0] = Name des Python Skripts
SysArgv[1] = Name des Sportler-Logs
SysArgv[2] = Name für die hier generierte csv-Datei
SysArgv[3] = Startposition, -1 für ab Anfang
SysArgv[4] = Endposition, -1 für bis Ende
SysArgv[5] = Soll Interpoliert werden? yes oder no

'''
interpol = "yes"


def getAttrBase(entry):
	zeitUnix = int(entry.getElementsByTagName('Timestamp')[0].firstChild.nodeValue)/1000.0
	zeitDate = datetime.utcfromtimestamp(zeitUnix).strftime("%Y-%m-%d %H:%M:%S")
	accuracy = float(entry.getElementsByTagName('Accuracy')[0].firstChild.nodeValue)
	speed = float(entry.getElementsByTagName('Speed')[0].firstChild.nodeValue)*3.6
	altitude = float(entry.getElementsByTagName('Altitude')[0].firstChild.nodeValue)
	bearing = float(entry.getElementsByTagName('Bearing')[0].firstChild.nodeValue)
	return (zeitUnix,zeitDate,accuracy,speed,altitude,bearing)

def analysiereElement(entry,csvWriter):
	(platzhalter, zeit, accuracy, speed, altitude, bearing) = getAttrBase(entry)
	csvWriter.writerow([zeit,accuracy,speed,altitude,bearing])


def accelPass():
	with open(sys.argv[2]) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		origLog = sys.argv[2]
		origLogNameLength = len(origLog)
		newLogName = origLog[:origLogNameLength-4] + "wAccel.csv"
		with open(newLogName, mode = 'w') as csvWritedatei:
			csvWriter = csv.writer(csvWritedatei, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)			
			csvWriter.writerow(['Time','Accuracy','Speed','Altitude','Bearing','SpeedDiffToLast','Acceleration'])
			runner = 0
			rowList = []
			for row in csv_reader:
				if runner > 0:
					rowList.append(row)
				runner = runner+1
			runner = 0
			
			smoothSpeedMin1 = float(rowList[1][2])
			for x in range(1,len(rowList)-3):
				current = rowList[x]
				time = current[0]
				neueAcc		= round(float(current[1]),3)
				neueSpeed 	= round(float(current[2]),3)
				neueAlt 	= round(float(current[3]),3)
				neueBear	= round(float(current[4]),3)

				speedDiffAv = (neueSpeed - smoothSpeedMin1)/3.6
				acceleration = speedDiffAv/9.81
				smoothSpeedMin1 = neueSpeed
				csvWriter.writerow([time,neueAcc,neueSpeed,neueAlt,neueBear,speedDiffAv,acceleration])
				runner = runner+1


def lint1(a, b, f):
	return (float(a) * (1.0 - float(f))) + (float(b) * float(f))

def interpolAndRound(a,b,f):
	ret = round(lint1(a,b,f),3)
	return ret

def analysiereOhneInterpolAuto(csvWriter, entryList,start,end):
	for x in range(start,end):
		analysiereElement(entryList[x],csvWriter)
	
def analysiereMitInterpol(csvWriter,entryList,start,end):
	if start == 0:
		start = start+1
	for x in range(start,end):
		previous = entryList[x-1]
		entry = entryList[x]
		(entryZeit,zeit,accuracy,speed,altitude,bearing) = getAttrBase(entry)
		(previousZeit,platzhalter1,previousAcc,previousSpeed,previousAlt,previousBear) = getAttrBase(previous)
		
		toReplace = entryZeit - previousZeit - 1
		if toReplace > 0.01:
			for i in range(0,int(toReplace)):
				interFaktor = (i+1) / toReplace
				nzeit = previousZeit + i + 1
				nzeit = datetime.utcfromtimestamp(nzeit).strftime("%Y-%m-%d %H:%M:%S")
				naccuracy = interpolAndRound(previousAcc,accuracy,interFaktor)
				nspeed = interpolAndRound(previousSpeed,speed,interFaktor)
				naltitude = interpolAndRound(previousAlt,altitude,interFaktor)
				nbearing = interpolAndRound(previousBear,bearing,interFaktor)
				csvWriter.writerow([nzeit,naccuracy,nspeed,naltitude,nbearing])
		csvWriter.writerow([zeit,accuracy,speed,altitude,bearing])

def analysiereTrack(entryList):
	start = int(sys.argv[3])
	end = int(sys.argv[4])
	if end == -1:
		end = entryList.length-1
	if start == -1:
		start = 0
	print(start)
	print(end)
	with open(sys.argv[2], mode = 'w') as csvWritedatei:
		csvWriter = csv.writer(csvWritedatei, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
		csvWriter.writerow(['Time','Accuracy','Speed','Altitude','Bearing'])
		if interpol == "yes":
			analysiereMitInterpol(csvWriter,entryList,start,end)
		else:
			analysiereOhneInterpolAuto(csvWriter,entryList,start,end)
	accelPass()
		

def leseSportlerTrack():
	print("leseSportlerTrack")
	print(sys.argv[1])
	dom = parse(sys.argv[1])
	entryList = dom.getElementsByTagName('LogEntry')
	if len(sys.argv) >= 6:
		interpol = sys.argv[5]
		#possible: "yes" = interpolate missing time; "no" = dont interpolate
	print(interpol)
	analysiereTrack(entryList)
	print("Fertig")
			

leseSportlerTrack()

#		#print(entryList[2].getElementsByTagName('Accuracy')[0].firstChild.nodeValue)
		#testZeit = int(entryList[2].getElementsByTagName('Timestamp')[0].firstChild.nodeValue)
		#print(datetime.utcfromtimestamp(testZeit).strftime('%Y-%m-%d %H:%M:%S'))
		#testZeit = testZeit/1000
		#print(testZeit)
		#print(datetime.utcfromtimestamp(testZeit))
		#Schreiben welche Eigenschaften/Header
