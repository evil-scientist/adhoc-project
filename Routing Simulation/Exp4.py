import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy


numberOfNodes = int(raw_input("How many nodes are in the graph?"))
probability = float(raw_input("what is the probability of edge existence?"))

g = nx.erdos_renyi_graph(numberOfNodes,probability)
AdjacencyMatrix = nx.adjacency_matrix(g)
AdjacencyMatrix = nx.to_numpy_matrix(g)
AdjacencyMatrix = AdjacencyMatrix.tolist()
#print(AdjacencyMatrix)

#print(AdjacencyMatrix[1])

  

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
	
	
#initialise elements
typeFlag, source, destination, sequence, metric, intermediary,data = 1,1,1,1,1,1,1
packet = [typeFlag, source, destination, sequence, metric, intermediary,data]

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
	source = int(raw_input("What is the source node?"))
	destination = int(raw_input("What is the destination?"))
	
	
	path.append(source)
	while ((nodeList[source].rNextHop[destination])!=(nodeList[source].rNextHop[source])):
		nextHop = nodeList[source].rNextHop[destination]
		path.append(nextHop)
		#print(nextHop)
		nodeList[source].sendPacket(nodeList[source].createPacket(1,source,destination,[],[],nextHop,"yes") )
		source = nextHop
	
	
	for node in g:
		if node in path:
			color_map.append('blue')
		else: color_map.append('green') 
	
	
	print (path)	
	
	pos = nx.spring_layout(g)
	path_edges = zip(path,path[1:])
	
	nx.draw(g,pos, node_color='green', with_labels = True)
	#nx.draw(g, node_color = color_map, with_labels=True)
	nx.draw_networkx_nodes(g,pos,nodelist=path,node_color='blue')
	nx.draw_networkx_edges(g,pos,edgelist=path_edges,edge_color='purple',width=5)
	plt.draw()
	plt.show()
		

main()

