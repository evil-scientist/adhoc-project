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
		g = routing.editGraphDistance(g,pos)
		routing.plotDistribution(g,pos)

        
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
        #routing.editGraphDistance(g,pos)
        routing.plotGraph(g,pos)
    elif button == 'Change Topology':
		app.showSubWindow('Topology Change')	
    else:        
        global nodeList
        global g        
        returnDict = routing.listRoute(g,pos,numberOfNodes)
        nodeList = returnDict["nodeList"]
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
app.addButtons(['Show Graph','Route', 'Change Topology'],graphPress)
app.setButtonFont(16,'Times')
app.stopSubWindow()
###<<<------------------->>>###

#Routing Window        
def getRoute(button):
	if button == 'Exit':
		app.hideSubWindow('Routing')
		app.showSubWindow('Graph')
	else:
		global nodeList
		source = int(app.getEntry('Source Node'))
		destination = int(app.getEntry('Destination Node'))
		path = routing.routeRoute(g,pos,nodeList,source,destination)        	
		routing.showRoute(g,pos,path)	

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


#Topology Change Window        
def graphChange(button):
    if button == 'Change':
		deleteNode = int(app.getEntry('Node To Delete'))
		global g
		global numberOfNodes
		global nodeList
		returnDict = routing.changeTopology(g,pos,deleteNode,numberOfNodes)
		g = returnDict["g"]
		nodeList = returnDict["nodeList"]
    elif button == 'Show Changed Graph':
		routing.plotGraph(g,pos)
    elif button == 'Reroute':
		app.hideSubWindow('Topology Change')
		app.showSubWindow('Routing')
    else:        
       pass

###<<< Topology Window >>>###
app.startSubWindow('Topology Change', modal=True)
app.setBg('Orange')
app.setGeometry("400x200")
app.setFont(18)
app.addLabel('title6','    Topology Change Mode    ')
app.setLabelBg('title6','blue')
app.setLabelFg('title6','white')
#Label Entries
app.addLabelEntry('Node To Delete')
#Buttons
app.addButtons(['Change','Show Changed Graph', 'Reroute'],graphChange)
app.setButtonFont(16,'Times')
app.stopSubWindow()
###<<<------------------->>>###
<<<<<<< HEAD
'''
=======



>>>>>>> 3d9f7de69c17e13e772d9acf868f2c88cc820353
#Scale Free Graph Window        
def getDataScaleFree(button):
	if button == 'Continue':
		app.hideSubWindow('Scale Free Graph')
		app.showSubWindow('Graph')
	else:
		global numberOfNodes 
		numberOfNodes = int(app.getEntry('No of Nodes'))
		#global probability 
		#probability = float(app.getEntry('Probability of Link'))
        
		print('\n\nThe graph will have: ' + str(numberOfNodes) + ' nodes')
		#print('The graph will have: ' + str(probability) + ' probability of link existence\n\n')
        	
		global g
		global pos 
		g = nx.barabasi_albert_graph(numberOfNodes,3, seed = 3)
		pos = nx.spring_layout(g) #define graph layput so node positions stay the same from plot to plot
		g = routing.edgeWeight(g,pos)
		routing.plotDistribution(g,pos)

###<<< Scale Free Graph Window >>>###
app.startSubWindow('Scale Free Graph', modal=True)
app.setBg('Orange')
app.setGeometry("400x200")
app.setFont(18)
app.addLabel('title3','    Scale Free Graph Mode    ')
app.setLabelBg('title3','blue')
app.setLabelFg('title3','white')
#Label Entries
app.addLabelEntry('No of Nodes')
#Buttons
app.addButtons(['Generate Graph','Continue'],getDataScaleFree)
app.setButtonFont(16,'Times')
app.setFocus('No of Nodes')
app.stopSubWindow()
###<<<------------------->>>###



#starting main GUI
app.go()


