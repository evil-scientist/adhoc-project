import os

AdjacencyMatrix = [[0,1,0,0,0,1,0,0,0,0],
                   [1,0,1,0,0,0,0,0,0,0],
                   [0,1,0,1,1,0,0,0,0,0],
                   [0,0,1,0,0,0,0,0,1,1],
                   [0,0,1,0,0,1,1,0,0,0],
                   [1,0,0,0,1,0,0,0,0,0],
                   [0,0,0,0,1,0,0,1,0,0],
                   [0,0,0,0,0,0,1,0,0,0],
                   [0,0,0,1,0,0,0,0,0,0],
                   [0,0,0,1,0,0,0,0,0,0]]

def shortestPath(AdjacencyMatrix,sourceNode):
	i = 0 
	m = 1 #used to increasingly find neighbours of neighbours
	visitedList = []
	sourceList = [999,999,999,999,999,999,999,999,999,999]; # stores the lenght of the shrtest path
	sourceList[sourceNode] = (min(sourceList[sourceNode],0))
	
	intermediateList = [999,999,999,999,999,999,999,999,999,999]; #stores the first nexthop in the shortest path
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
	



#source
#destination

#typeflag = 1 update, typeflag = 0 data
#initialise elements
typeFlag, source, destination, sequence, metric, intermediary,data = 1,1,1,1,1,1,1
packet = [typeFlag, source, destination, sequence, metric, intermediary,data]

class adHocNode(object):
	def __init__(self,MACAddress,rDestination =[1,2,3,4,5,6,7,8,9,10],rSequence=[],rMetric=[],rNextHop=[]):
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
	node0 = adHocNode(0)
	node1 = adHocNode(1)
	node2 = adHocNode(2)
	node3 = adHocNode(3)
	node4 = adHocNode(4)
	node5 = adHocNode(5)
	node6 = adHocNode(6)
	node7 = adHocNode(7)
	node8 = adHocNode(8)
	node9 = adHocNode(9)
	
		
	nodeList = [node0,node1,node2,node3,node4,node5,node6,node7,node8,node9]
			
	
	for item in nodeList:
		item.rNextHop = shortestPath(AdjacencyMatrix,item.MACAddress)
		print item.MACAddress
		print item.rDestination
		print item.rNextHop
		
	#user input source and destination and data
	print("Got a message to send?")
	print("Follow the prompt")
	source = int(raw_input("What is the source node?"))
	destination = int(raw_input("What is the destination?"))
	

	while ((nodeList[source].rNextHop[destination])!=(nodeList[source].rNextHop[source])):
		nextHop = nodeList[source].rNextHop[destination]
		#print(nextHop)
		nodeList[source].sendPacket(nodeList[source].createPacket(1,source,destination,[],[],nextHop,"yes") )
		source = nextHop
		

main()

