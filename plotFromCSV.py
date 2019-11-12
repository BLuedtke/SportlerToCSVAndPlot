#!/usr/bin/python3
import sys
from xml.dom.minidom import parse, parseString
import csv
from datetime import datetime
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import scipy

from scipy import signal


def smoothTriangle(data, degree):
    triangle=np.concatenate((np.arange(degree + 1), np.arange(degree)[::-1])) # up then down
    smoothed=[]

    for i in range(degree, len(data) - degree * 2):
        point=data[i:i + len(triangle)] * triangle
        smoothed.append(np.sum(point)/np.sum(triangle))
    # Handle boundaries
    smoothed=[smoothed[0]]*int(degree + degree/2) + smoothed
    while len(smoothed) < len(data):
        smoothed.append(smoothed[-1])
    return smoothed

def diffToLast(data):
	 pass

def main():
	df = pd.read_csv(sys.argv[1])
	fig3 = make_subplots(specs=[[{"secondary_y": True}]])
	
	#Sysargv[2] = Name der Spalte die dargestellt werden soll
	#Sysargv[3] = none, low, medium, high

	if len(sys.argv) >= 4:
		if sys.argv[3] == "high":
			fig3.add_scatter(x=df.Time, y=signal.savgol_filter(df[sys.argv[2]],50,4),secondary_y=False, name=sys.argv[2])
		elif sys.argv[3] == "medium":
			fig3.add_scatter(x=df.Time, y=signal.savgol_filter(df[sys.argv[2]],25,4),secondary_y=False, name=sys.argv[2])
		elif sys.argv[3] == "low":
			fig3.add_scatter(x=df.Time, y=signal.savgol_filter(df[sys.argv[2]],10,4),secondary_y=False, name=sys.argv[2])
		elif sys.argv[3] == "none":
			fig3.add_scatter(x=df.Time, y=df[sys.argv[2]],secondary_y=False,name=sys.argv[2])




	#das hier war das vorher:
	#fig3.add_scatter(x=df.Time, y=signal.savgol_filter(df.SpeedDiff,17,3),secondary_y=True, name="gs17")
	
	#fig3.add_scatter(x=df.Time, y=df.Speed,secondary_y=False,name="NoSmoothSpeed")
	if len(sys.argv) >= 3:
		fig3.add_scatter(x=df.Time, y=signal.savgol_filter(df[sys.argv[2]],19,4),secondary_y=False, name="sys.argv[2]")
	else:
		fig3.add_scatter(x=df.Time, y=signal.savgol_filter(df['SpeedDiff'],17,3),secondary_y=True, name="gs17")
	#fig3.add_scatter(x=df.Time, y=smoothTriangle(df.Speed,3),secondary_y=False, name="SpeedTri")
	
	fig3.show()

main()