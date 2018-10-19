#! Python3
import time
import csv
import serial
import matplotlib.pyplot as plt
from appJar import gui

import os, random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy, math
#import seaborn as sns


###<<< GUI CODE >>>###

#Main Menu Window
def graphChoose(button):
    if button == 'Random Graph':
        #app.stop()
        print('You have chosen Random Graph Mode')
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
    if button == 'Cancel':
        app.hideSubWindow('Random Graph')
    else:
        numberOfNodes = app.getEntry('Number of Nodes')
        probability = app.getEntry('Probability of Link')
        #global file_name
        #file_name = name + '_' + gesture + '.csv'
        print('The graph will have: ' + numberOfNodes + ' nodes')
        print('The graph will have: ' + probability + ' probability of link existence')
        g = nx.erdos_renyi_graph(numberOfNodes,probability)
        pos = nx.spring_layout(g) #define graph layput so node positions stay the same from plot to plot
        #app.showSubWindow('Graph')

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
app.addButtons(['Enter','Cancel'],getDataRandom)
app.setButtonFont(16,'Times')
app.setFocus('Number of Nodes')
app.stopSubWindow()
###<<<------------------->>>###

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

#Readings Window
'''
def windowPress(button):
    if button == 'Finish':
        #filecreating(analog_reads,file_name)
        #plt.close()
        app.hideSubWindow('Readings')
    else:
        emg()
        #print('Reached readings code')
        app.hideSubWindow('Readings')

###<<< Readings Window >>>###         

app.startSubWindow('Readings', modal=True)
app.setBg('Orange')
app.setGeometry("400x200")
app.setFont(18)
app.addLabel('promt','Click Start to begin taking readings')
app.setLabelFg('promt','white')
app.setLabelBg('promt','blue')
app.addMeter('Readings')
app.setMeterFill('Readings','red')        
app.addButtons(['Start','Finish'],windowPress)
app.stopSubWindow()
'''
###<<<------------------->>>###

def plotting(x,y):
    plt.plot(x,y)
    plt.show()

def filecreating(output,file):
    print('csv function called')
    myfile = open(file,'w')
    with myfile:
        writer = csv.writer(myfile)
        writer.writerow(output)    

def emg():
    print('Readings starting now: ')
        
#starting main GUI
app.go()


