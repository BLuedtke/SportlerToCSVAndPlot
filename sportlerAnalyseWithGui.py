#! /usr/bin/env python
#  -*- coding: utf-8 -*-

from tkinter import *
import subprocess

def evalIntpolEntr():
	interpolEntry = e5.get()
	if 'y' in interpolEntry:
		return "yes"
	else:
		return "no"

def evalSvFlEntr():
	saveFileName = e2.get()
	if saveFileName == "":
		print("ERROR! NO SUCH FILE")
		return "placeholder.csv"
	if '.csv' in saveFileName:
		return saveFileName
	else:
		return (saveFileName+".csv") 

def evalFileNameForGraph():

	origLog = evalSvFlEntr()
	origLogNameLength = len(origLog)
	newLogName = origLog[:origLogNameLength-4] + "wAccel.csv"

def startProcessing():
	print("Start startProcessing")
	loadFileName = e1.get()
	startPos = e3.get()
	endPos = e4.get()
	subprocess.run(["python","./sportlerXMLtoCSV.py",loadFileName,evalSvFlEntr(),startPos,endPos,evalIntpolEntr()])

def show_entry_fields():
	subprocess.run(["python","./plotFromCSV.py","wAccel"+evalSvFlEntr(),dropDownVar1.get()])
	#print("Name of sportler File: %s\nName of SaveFile: %s" % (e1.get(), e2.get()))

master = Tk()
Label(master, text="Name of sportler File").grid(row=0)
Label(master, text="Name of SaveFile").grid(row=1)
Label(master, text="Start Position (int)").grid(row=2)
Label(master, text="End Position (int)").grid(row=3)
Label(master, text="Interpolate missing? 'yes'/'no'").grid(row=4)


e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e1.insert(10,"sportler_track_03.01.19_09_38.spt")
e3.insert(10,"-1")
e4.insert(10,"-1")
e5.insert(10,"yes")


e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)

Label(master, text="Generate CSV").grid(row=5)

Button(master, text='Execute', command=startProcessing).grid(row=5, column=1, sticky=W, pady=4)

Label(master, text="Plot Category").grid(row=6)

graphOpt = ['Time','Accuracy','Speed','Altitude','Bearing','SpeedDiffToLast','Acceleration']
dropDownVar1 = StringVar(master)
dropDownVar1.set("Speed") # default
dropDownEntity1 = OptionMenu(master,dropDownVar1,*graphOpt)
dropDownEntity1.grid(row=6,column=1)

Label(master, text="Generate Plot").grid(row=8)
Button(master, text='Show', command=show_entry_fields).grid(row=8, column=1, sticky=W, pady=4)

Label(master, text="Plot Smoothing").grid(row=7)

smoothOpt = ['none','low','medium','high']
dropDownVar2 = StringVar(master)
dropDownVar2.set("medium") # default
dropDownEntity2 = OptionMenu(master,dropDownVar2,*smoothOpt)
dropDownEntity2.grid(row=7,column=1)

mainloop( )
