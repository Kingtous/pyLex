import networkx as nx
import os

def writeGraph2File(multidigraph,filePath):
    nx.nx_pydot.write_dot(multidigraph,filePath)

def convertGraphFile2PDF(filePath,pdfName):
    if not os.path.exists(filePath):
        return False
    os.system('dot -Tpdf '+filePath+' -o'+pdfName)

def addEdgesToGraph(multidigraph,lis):
    for tri_arr in lis:
        multidigraph.add_edge(tri_arr[0],tri_arr[2],label=tri_arr[1])
