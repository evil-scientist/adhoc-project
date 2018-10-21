import os, random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy, math
#import seaborn as sns

def eucledianDistanceBetweenNodes(g,pos):
	#this function takes the graph as input and finds eucledian distance between each nodes with a link
	#this is used later when we delete links between nodes that are too far apart
	#this adds a distance dependence to the random graph geenrated
	lengths={}
	for edge in g.edges():
		startnode=edge[0] 
		endnode=edge[1]
		lengths[edge]=round(math.sqrt(((pos[endnode][1]-pos[startnode][1])**2)+((pos[endnode][0]-pos[startnode][0])**2)),2)	
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

def plotDistribution(g,pos):
	lengths = eucledianDistanceBetweenNodes(g,pos)
	plt.bar(range(len(lengths.keys())), list(lengths.values()), color='g')
	plt.ylabel('Link Probability')
	plt.xlabel('Number of Nodes')	
	plt.title('Link Probability Distribution')	
	plt.show()

def plotGraph(g,pos):
	labels = [g[u][v]['weight'] for u,v in g.edges]
	weights = nx.get_edge_attributes(g,'weight')
	nx.draw(g,pos, node_color='green', edge_color='grey', width=labels, with_labels = True, alpha = 0.5)
	nx.draw_networkx_edge_labels(g,pos,edge_labels = weights)
	plt.title('Network Graph')
	plt.show()

def shortestPath(AdjacencyMatrix,sourceNode,numberOfNodes):
	i = 0 
	m = 1 #used to increasingly find neighbours of neighbours
	visitedList = []
	sourceList = []
	intermediateList = []
	costList = []
	
	sourceList += ([999] * numberOfNodes) # stores the lenght of the shrtest path but strats out with all 999 values(djikstra)
	sourceList[sourceNode] = (min(sourceList[sourceNode],0))
	
	
	intermediateList += ([999] * numberOfNodes) #stores the first nexthop in the shortest path
	intermediateList[sourceNode] = sourceNode #for the source node it's next hop is itself (this is the condition to stop routing)
			
	Q = [i for i in range(numberOfNodes)]
	u = sourceNode
	
	while Q:
		Q.remove(u)
		#u is newest removed member
		
		check = [value for value in AdjacencyMatrix[u] if value > 0 and AdjacencyMatrix[u].index(value) in Q]
		if check:
			i = 0
			for row in AdjacencyMatrix[u]:
				#k = AdjacencyMatrix[u].index(min(check))
				if row > 0:
					if (min(sourceList[i],row+sourceList[u])) == (row + sourceList[u]):
						sourceList[i] = (min(sourceList[i],AdjacencyMatrix[u][i]+sourceList[u]))
						intermediateList[i] = u #add this node to the path list
				i+=1
				
		value = {}
		for k in range(numberOfNodes):

			if k in Q:
				value.update({k:sourceList[k]})
		if value:
			u = min(value, key =value.get)
		else:
			if len(Q) == 1:
				Q.remove(Q[0])
		
		#u = k
		#print k
		#print ("Q list",Q)
			
	
	#reconstruct path
	pathTaken = [[] for i in range(numberOfNodes)]
		
	p = 0
	count = 0
	for element in intermediateList:
		elementValue = element
		pathTaken[p].append(p)
		pathTaken[p].append(elementValue)
		while pathTaken[p][-1] != sourceNode:
			pathTaken[p].append(intermediateList[elementValue])
			elementValue = intermediateList[elementValue]
		p+=1
		#count +=1 
					
	for i in range(numberOfNodes):
		visitedList.append(pathTaken[i][-2])
	#print(sourceNode)
	#print("Cost List is", sourceList)
	#print("Path Taken is", pathTaken)
	#print("Visited List is", visitedList)
	
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
		
    
def listRoute(g,pos,numberOfNodes):
	
	#this series of actions provides the adjacency matrix as a list of lists
	#so we can iterated through them for paths and rputing later
	AdjacencyMatrix = nx.adjacency_matrix(g)
	AdjacencyMatrix = nx.to_numpy_matrix(g)
	AdjacencyMatrix = AdjacencyMatrix.tolist()
  
	#initialise elements
	typeFlag, source, destination, sequence, metric, intermediary,data = 1,1,1,1,1,1,1
	packet = [typeFlag, source, destination, sequence, metric, intermediary,data]
			
	color_map = []
	
	nodeList = []
	for i in range(numberOfNodes):
		nodeList.append(adHocNode(i))
	
	#print(nodeList)
	destinationList = []
	destinationList.extend(range(numberOfNodes))
			
	
	for item in nodeList:
		item.rDestination = destinationList
		item.rNextHop = shortestPath(AdjacencyMatrix,item.MACAddress,numberOfNodes)
		print (item.MACAddress)
		print (item.rDestination)
		print (item.rNextHop)
  			
	return nodeList

def routeRoute(g,pos,nodeList, source, destination):
	path = [] #path that packet takes. saved as a list for the plot		
	#nx.draw(g,pos, node_color='green', edge_color='grey', with_labels = True, alpha = 0.5) #draw the network
	path.append(source)
	while ((nodeList[source].rNextHop[destination])!=(nodeList[source].rNextHop[source])):
		nextHop = nodeList[source].rNextHop[destination]
		path.append(nextHop)
		nodeList[source].sendPacket(nodeList[source].createPacket(1,source,destination,[],[],nextHop,"yes") )
		source = nextHop
	print (path)
	return path
	

def showRoute(g,pos,path):
	path1=[]
	for i in range(len(path)):
		plt.gcf().clear()
		path1.append(path[i])
		#print("inloop")
		
		labels = [g[u][v]['weight'] for u,v in g.edges]
		weights = nx.get_edge_attributes(g,'weight')
		nx.draw(g,pos, node_color='green', edge_color='grey', width=labels, with_labels = True, alpha = 0.5)
		nx.draw_networkx_edge_labels(g,pos,edge_labels = weights)
		
		path_edges = zip(path,path[1:])
		nx.draw_networkx_nodes(g,pos,nodelist=path1,node_color='blue')
		nx.draw_networkx_edges(g,pos,edgelist=path_edges,edge_color='purple')
			
		plt.draw()
		plt.pause(1)
		
	plt.show()

#remove a node and repeat process
#g.remove_node(1)
#numberOfNodes -= 1

