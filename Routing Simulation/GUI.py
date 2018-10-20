#! Python3
import time
import csv
import serial
import matplotlib.pyplot as plt
from appJar import gui

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
	if button == 'Proceed':
		app.hideSubWindow('Random Graph')
		app.showSubWindow('Graph')
	else:
		numberOfNodes = int(app.getEntry('Number of Nodes'))
		probability = float(app.getEntry('Probability of Link'))
        #global file_name
        #file_name = name + '_' + gesture + '.csv'
		print('\n')
		print('The graph will have: ' + str(numberOfNodes) + ' nodes')
		print('The graph will have: ' + str(probability) + ' probability of link existence')
        
		global g
		global pos 
		g = nx.erdos_renyi_graph(numberOfNodes,probability)
		pos = nx.spring_layout(g) #define graph layput so node positions stay the same from plot to plot
		editGraphDistance(g,pos)
		

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
    if button == 'Cancel.':
        app.hideSubWindow('Scale Free Graph')
    else:
        main(g)

###<<< Scale Free Graph Window >>>###
app.startSubWindow('Graph', modal=True)
app.setBg('Orange')
app.setGeometry("400x200")
app.setFont(18)
app.addLabel('title4','    Graph Mode    ')
app.setLabelBg('title4','blue')
app.setLabelFg('title4','white')
#Buttons
app.addButtons(['Start','Cancel'],graphPress)
app.setButtonFont(16,'Times')
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
def eucledianDistanceBetweenNodes(g,pos):
	#this function takes the graph as input and finds eucledian distance between each nodes with a link
	#this is used later when we delete links between nodes that are too far apart
	#this adds a distance dependence to the random graph generated
	lengths={}
	for edge in g.edges():
		startnode=edge[0] 
		endnode=edge[1]
		lengths[edge]=round(math.sqrt(((pos[endnode][1]-pos[startnode][1])**2)+((pos[endnode][0]-pos[startnode][0])**2)),2)
	
	plt.bar(range(len(lengths.keys())), list(lengths.values()), color='g')
	plt.ylabel('some numbers')
	plt.xlabel('some numbers')
	plt.title('some graph')
	plt.show()

	return lengths


def editGraphDistance(g,pos):
	#this function deletes edges that are longer than 1/2 the maximum edge length that was randomly generated
	lengths = eucledianDistanceBetweenNodes(g,pos)
	maximumDistance = max(list(lengths.values()))
	#print (lengths)
	for i,j in lengths.items():
		if j > (maximumDistance/2):
			#print(i,":",j)
			g.remove_edge(i[0],i[1])
			
	#randomly assigning edge weights
	for edge in g.edges():
		startnode = edge[0]
		endnode = edge[1]
		g[startnode][endnode]['weight']=random.randint(1,11)


def shortestPath(AdjacencyMatrix,sourceNode):
	i = 0 
	m = 1 #used to increasingly find neighbours of neighbours
	visitedList = []
	sourceList = []
	intermediateList = []
	
	sourceList += ([999] * numberOfNodes) # stores the lenght of the shrtest path but strats out with all 999 values(djikstra)
	sourceList[sourceNode] = (min(sourceList[sourceNode],0))
	
	intermediateList += ([999] * numberOfNodes) #stores the first nexthop in the shortest path
	intermediateList[sourceNode] = sourceNode #for the source node it's next hop is itself (this is the condition to stop routing)
	
	
	for row in AdjacencyMatrix[sourceNode]: #loops through the node in question(i.e. that row of the adjacency matrix)
		if row == 1: #finds neighbours of source node
			sourceList[i] = (min(sourceList[i],row)) #set distance to 1 in source list
			intermediateList[i] = i #add this node to the path list
		i+=1
		
		
	while 999 in sourceList:
		j = 0
		for row in sourceList:
			k = 0
			if row == m:			#for rows that have been found to be neighbours...and then iterates for neighbours of neighbours..ati be be lo	
				for val in AdjacencyMatrix[j]:
					if val == 1:
						if (min(sourceList[k],(m+1)*val)) == (m+1)*val:
							sourceList[k] = (min(sourceList[k],(m+1)*val))
							intermediateList[k] = intermediateList[j] #copy the path to its predecessor
							#intermediateList[k].append(intermediateList[j][-1])
					k += 1
			j+=1
		m+=1
	
	visitedList = intermediateList
	#print(sourceNode)
	#print(sourceList)
	#print(intermediateList)
	
	return visitedList
	
	
class adHocNode(object):
	def __init__(self,MACAddress,rDestination =[],rSequence=[],rMetric=[],rNextHop=[]):
		self.MACAddress = MACAddress
		self.rDestination = rDestination
		self.rSequence = rSequence
		self.rMetric = rMetric
		self.rNextHop = rNextHop
		routingTable = [rDestination,rSequence,rMetric,rNextHop]
		self.routingTable = routingTable
	
	#functions
	
	def sendPacket(self,Packet):
		print("Packet forwarded to node ",Packet[5])
	def createPacket(self,typeFlag, source, destination, sequence, metric, nextHop,data):
		Packet = [typeFlag, source, destination, sequence, metric, nextHop, data]
		return Packet
	def onReceive(self,Packet):
		print("in on recieve")
		if Packet[0] == 1:
			destinationr = Packet[2]
			intermediaryr = Packet[5]
			if destinationr == self.MACAddress:
				print("Yayyyyyy I got my packet")
			elif intermediaryr == self.MACAddress:
				if destinationr in self.rDestination:
					positionr = rDestination.index(destinationr)
					nextHopr = self.rNextHop[positionr]
					sendPacket(Packet[0],Packet[1],Packet[2],sequence, metric,nextHopr,data);	
		elif Packet[1] == 0:
			print("Update Packet")
			#updateTable(Packet)
		
    
def main():
	
	path = [] #path that packet takes. saved as a list for the plot
	color_map = []
	
	nodeList = []
	for i in range(numberOfNodes):
		nodeList.append(adHocNode(i))
		
	destinationList = []
	destinationList.extend(range(numberOfNodes))
			
	
	for item in nodeList:
		item.rDestination = destinationList
		item.rNextHop = shortestPath(AdjacencyMatrix,item.MACAddress)
		#print item.MACAddress
		#print item.rDestination
		#print item.rNextHop
		
	#user input source and destination and data
	print("Got a message to send?")
	print("Follow the prompt")
	source = int(input("What is the source node?"))
	destination = int(input("What is the destination?"))
	
	
	#nx.draw(g,pos, node_color='green', edge_color='grey', with_labels = True, alpha = 0.5) #draw the network
	
	path.append(source)
	while ((nodeList[source].rNextHop[destination])!=(nodeList[source].rNextHop[source])):
		nextHop = nodeList[source].rNextHop[destination]
		path.append(nextHop)
		nodeList[source].sendPacket(nodeList[source].createPacket(1,source,destination,[],[],nextHop,"yes") )
		source = nextHop
	print (path)
	
	path1=[]
	
	for i in range(len(path)):
		plt.gcf().clear()
		path1.append(path[i])
		#print("inloop")
		nx.draw(g,pos, node_color='green', edge_color='grey', with_labels = True, alpha = 0.5)
		path_edges = zip(path,path[1:])
		nx.draw_networkx_nodes(g,pos,nodelist=path1,node_color='blue')
		nx.draw_networkx_edges(g,pos,edgelist=path_edges,edge_color='purple',width=1)
			
		plt.draw()
		plt.pause(1)
		
	plt.show()
			
	#return path	
	

def plotPath(i):
	
	path_edges = zip(path,path[1:])
	nx.draw_networkx_nodes(g,pos,nodelist=path[i],node_color='blue')
	#nx.draw_networkx_edges(g,pos,edgelist=path_edges[i],edge_color='purple',width=5)
		
     



#starting main GUI
app.go()


