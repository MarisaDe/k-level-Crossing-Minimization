# Name: Marisa DePasquale
# ID: 109075332
###################################################

import fileinput  # opens the file based on the console
import itertools
import Layer
import re

layers = []         #will hold our list of layers.
width = None        #placeholder width to fill for each layer
nodes = []          #holds array of all nodes between all layers
nodesDict = {}      #Stores info about all nodes and their edges
edges = []          #holds array of all edges between all layers
numLayers = 0       #store number of layers
arrayMat = []       #Array of matrices where each matrix has 1's for an edge inbetween 2 layers
permMat = []        #Stores a list of matrices where each matrix has a list of all permutations for that layer index
minC = -1           #keeps track of min. pair of crossing
cross1 = -1           #sum for lay1
cross2 = -1           #sum for lay2


# Parses input file information
#####################################################################################
for line in fileinput.input():                                          #goes through the input file
    if "layers" in line:
        numLayers = line.split('(', 1)[1].split(')')[0]                 #gets the number of layers.
        for count in range(int(numLayers)):                             #creates layer objects.
            x = Layer.Layer()
            x.level = count
            layers.append(x)


    if "width" in line:
        i = int((line.split('(', 1)[1].split(',')[0]))                  #tells which layer object to put it in
        width = int((line.split(',', 1)[1].split(')')[0]))              #tells how many nodes per layer
        layers[i-1].width = width;                                      #puts the correct width for each layer object


    if "in_layer" in line:
        i = int((line.split('(', 1)[1].split(',')[0]))                  #tells which layer object to put it in
        layers[i - 1].nodes[(line.split(',', 1)[1].split(')')[0])] = [] #tells which layer object to put the nodes in
        nodes.append(line.split(',', 1)[1].split(')')[0])               #collect full list of nodes
        nodesDict[(line.split(',', 1)[1].split(')')[0])] = []
        layers[i - 1].edges.append(0)                                   #init all nodes with 0 edge
        layers[i - 1].nodeArr.append((line.split(',', 1)[1].split(')')[0]))
        edges.append(0)                                                 #puts 0 in the edge list across all layers


    if "edge" in line:

        startedge = (line.split('(', 1)[1].split(',')[0])               #gets the first node of a edge
        i = nodes.index(startedge)
        edges[i] = edges[i] + 1
        endedge = (line.split(',', 1)[1].split(')')[0])                 #gets second node of an edge
        x = nodes.index(endedge)
        edges[x] = edges[x] + 1

        nodesDict[startedge].append(endedge)
        nodesDict[endedge].append(startedge)

for key in nodesDict:                                                   #Goes through all nodes (15 of em)
    for layNum in range(int(numLayers)):                                #Does 3 layers
        if key in layers[layNum].nodes:
            layers[layNum].nodes[key].append(nodesDict[key])            #Adds key value to the key


#Collects all permutations in a matrix list
for n in range(int(numLayers)): 
    x = list(itertools.permutations(layers[n].nodeArr)) 
    permMat.append(-1)
    permMat[n] = x



#Function that creates empty array of matrices
#######################################################################################
def clear():
    if len(arrayMat) > 0:
        del arrayMat[:]
    for i in range(int(numLayers)): #should make 2 arrays
        if i == int(numLayers)-1:
            break
        w = layers[i].width
        h = layers[i+1].width
        matrix = [[0 for x in range(w)] for y in range(h)]
        arrayMat.append(matrix)
    return;



#Function that fills the matrix with 1's for edges and counts all the crossings between 2 given layers
############################################################################################
def fillAndFindCrossings(matNum, minlayerCross):
    ########################################################################################
    #Fills the matrices with 1s for each edge
    i = 0
    for mat in range(len(arrayMat)):                                        #go through all the matrices(2 in the test case)
        for size in range(layers[i].width):                 
            node = layers[i].nodeArr[size]                                  #look at the nodes in the layer.
            for edge in layers[i].nodes[node]:
                if edge:
                    for values in edge:
                        if values in layers[i+1].nodeArr:
                            storeIndex = layers[i+1].nodeArr.index(values)   #got the index now we can populate the array
                            arrayMat[mat][size][storeIndex] = 1;
        i = i+1

    #######################################################################################
    ##Gathers all indices that have edges and put it in a list
    countrow = 0;
    countcol = []
    for row in arrayMat[matNum]:       
        indices = [i for i, x in enumerate(arrayMat[matNum][countrow]) if x == 1]
        for z in indices:
            layers[matNum].numedges += 1                                    #increase edge count in a layer
            countcol.extend((countrow, z))                                  #gathers indices
        countrow = countrow + 1


    ########################################################################################
    #Compares the list of indices with edges with each other to find crossings.
    crossing = 0
    rStart = 0;
    cStart = 1;
    r = 2;
    c = 3;
    rangee = int(len(countcol)/2)
    for n in range(rangee):                                                 
        while c < len(countcol) or r < len(countcol):
            if crossing > minlayerCross and minlayerCross >= 0:
                return -1;
            elif rStart >= r or cStart >= c or c >= len(countcol) or r >= len(countcol):
                break
            elif countcol[rStart] > countcol[r] and countcol[cStart] < countcol[c]:
                crossing += 1
            elif countcol[rStart] < countcol[r] and countcol[cStart] > countcol[c]:
                crossing += 1

            r += 2
            c += 2
        rStart +=2
        cStart += 2
        r = 2 + rStart
        c = 2 + cStart 
    return crossing;                    

##########################################################################################################
clear()                                                     #create empty array of matrices
#Fills in a node array for specified layer given a permutation
def onePermutation(n, row):
    count = 0                                                                       
    for eachVal in row:                                
        layers[n].nodeArr[count] = eachVal
        count += 1                                                   
    count = 0
    return;

for i in (itertools.product(*permMat)):                     #goes through whole giant list (each index has 3 lists)
    crossC = 0
    for index in range(int(numLayers)-1):                   #count between 2 layers
        onePermutation(index, i[index])                     #Fills nodes for 1st layer    
        onePermutation(index+1, i[index+1])                 #Fills nodes for 2nd layer
        clear()                                             #Empties out the matrix between the layers
        tempC = fillAndFindCrossings(index, minC)           #Fills the matrix and finds crossings
        if tempC == -1:
            crossC = -1
            break
        else:
            crossC += tempC    
    if (crossC < minC and crossC >= 0) or minC == -1:
        minC = crossC 
    if minC == 0:
        break    

print("Optimization:", minC)
fileinput.close()                                           #closes the input file