#! Python3
import time
import csv
import serial
import matplotlib.pyplot as plt
from appJar import gui

import warnings
import matplotlib.cbook

import routing
import os, random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy, math
###<<< GUI CODE >>>###

#Main Menu Window
def graphChoose(button):
    if button == 'Random Graph':
        #app.stop()
        print('\nYou have chosen Random Graph Mode\n')
        warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
        app.showSubWindow('Random Graph')
    else:
        app.showSubWindow('Scale Free Graph')

app = gui('AdHoc Network Creator v.1', '400x200')
app.setBg('Orange')
app.setLabelFont(16,'Times')
font = 'Times 16 normal'

#Labels
app.addLabel('title1','Choose the type of graph:')
app.setLabelBg('title1','red')
app.setLabelFg('title1','white')

#Buttons
app.addButtons(['Random Graph','Scale Free Graph'],graphChoose)
app.setButtonFont(16,'Times')


#Random Graph Window        
def getDataRandom(button):
	if button == 'Proceed':
		app.hideSubWindow('Random Graph')
		app.showSubWindow('Graph')
	else:
		global numberOfNodes 
		numberOfNodes = int(app.getEntry('Number of Nodes'))
		global probability 
		probability = float(app.getEntry('Probability of Link'))
        
		print('\n\nThe graph will have: ' + str(numberOfNodes) + ' nodes')
		print('The graph will have: ' + str(probability) + ' probability of link existence\n\n')
        	
		global g
		global pos 
		g = nx.erdos_renyi_graph(numberOfNodes,probability)
		pos = nx.spring_layout(g) #define graph layput so node positions stay the same from plot to plot
		routing.plotDistribution(g,pos)
		#routing.editGraphDistance(g,pos)
        

###<<< Random Graph Window >>>###
app.startSubWindow('Random Graph', modal=True)
app.setBg('Orange')
app.setGeometry("400x200")
app.setFont(18)
app.addLabel('title2','    Random Graph Mode    ')
app.setLabelBg('title2','blue')
app.setLabelFg('title2','white')
#Label Entries
app.addLabelEntry('Number of Nodes')
app.addLabelEntry('Probability of Link')
#Buttons
app.addButtons(['Generate','Proceed'],getDataRandom)
app.setButtonFont(16,'Times')
app.setFocus('Number of Nodes')
app.stopSubWindow()
###<<<------------------->>>###

#Graph Window        
def graphPress(button):
    if button == 'Show Graph':
        routing.editGraphDistance(g,pos)
        routing.plotGraph(g,pos)
    else:        
        global nodeList        
        nodeList = routing.listRoute(g,pos,numberOfNodes)
        app.hideSubWindow('Graph')
        app.showSubWindow('Routing')

###<<< Graph Window >>>###
app.startSubWindow('Graph', modal=True)
app.setBg('Orange')
app.setGeometry("400x200")
app.setFont(18)
app.addLabel('title4','    Graph Mode    ')
app.setLabelBg('title4','blue')
app.setLabelFg('title4','white')
#Buttons
app.addButtons(['Show Graph','Route'],graphPress)
app.setButtonFont(16,'Times')
app.stopSubWindow()
###<<<------------------->>>###

#Routing Window        
def getRoute(button):
	if button == 'Exit':
		app.hideSubWindow('Routing')
		app.showSubWindow('Graph')
	else:
		source = int(app.getEntry('Source Node'))
		destination = int(app.getEntry('Destination Node'))
		path = routing.routeRoute(g,pos,nodeList,source,destination)        	
		#routing.showRoute(g,pos,path)	

###<<< Routing Window >>>###
app.startSubWindow('Routing', modal=True)
app.setBg('Orange')
app.setGeometry("400x200")
app.setFont(18)
app.addLabel('title5','    Random Graph Mode    ')
app.setLabelBg('title5','blue')
app.setLabelFg('title5','white')
#Label Entries
app.addLabelEntry('Source Node')
app.addLabelEntry('Destination Node')
#Buttons
app.addButtons(['Show Route','Exit'],getRoute)
app.setButtonFont(16,'Times')
app.setFocus('Source Node')
app.stopSubWindow()
###<<<------------------->>>###
'''
#Scale Free Graph Window        
def getDataScaleFree(button):
    if button == 'Cancel.':
        app.hideSubWindow('Scale Free Graph')
    else:
        numberOfNodes = app.getEntry('No. of Nodes')
        #global file_name
        #file_name = name + '_' + gesture + '.csv'
        print('The graph will have: ' + numberOfNodes + 'nodes')
        #app.showSubWindow('Graph')

###<<< Scale Free Graph Window >>>###
app.startSubWindow('Scale Free Graph', modal=True)
app.setBg('Orange')
app.setGeometry("400x200")
app.setFont(18)
app.addLabel('title3','    Scale Free Graph Mode    ')
app.setLabelBg('title3','blue')
app.setLabelFg('title3','white')
#Label Entries
app.addLabelEntry('No. of Nodes')
#Buttons
app.addButtons(['Enter.','Cancel.'],getDataScaleFree)
app.setButtonFont(16,'Times')
app.setFocus('Number of Nodes')
app.stopSubWindow()
###<<<------------------->>>###
'''


#starting main GUI
app.go()


