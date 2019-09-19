import networkx as nx

def writeGraph2File(multidigraph,filePath):
    nx.nx_pydot.write_dot(multidigraph,filePath)

def convertGraphFile2PDF(filePath,pdfName):
    import os
    if not os.path.exists(filePath):
        return False
    os.system('dot -Tpdf '+filePath+' -o'+pdfName)

def addEdgesToGraph(multidigraph,lis):
    for tri_arr in lis:
        multidigraph.add_edge(tri_arr[0],tri_arr[2],label=tri_arr[1])

def expandMoveForGraph(multidigraph,oriSet,dir):
    """
    multidigraph : graph
    oriSet : ori Set of vertex
    dir : expand direction
    """
    import copy,constDef
    aSet = set()
    # 求move(I,dir)
    for vertex in oriSet:
        for nei in nx.neighbors(multidigraph,vertex):
            edata = multidigraph.get_edge_data(vertex,nei) # dict
            for ekey in edata.keys():
                data = edata[ekey]
                fresult = data.get(constDef.prop_label,constDef.ver_none)
                if fresult == constDef.ver_none:
                    import sys
                    sys.stderr.write('No Label From '+vertex+'To'+nei)
                    exit(-1)
                elif fresult == dir:
                    aSet.add(nei)
    return aSet

def expandEpsilonForGraph(multidigraph,oriSet):
    import constDef,copy
    pSet = copy.copy(oriSet)
    pSetSize = len(pSet)
    while True:
        pSet = pSet.union(expandMoveForGraph(multidigraph,pSet,constDef.eps))
        pSetSizeU = len(pSet)
        if pSetSizeU == pSetSize:
            break
        else:
            pSetSize = pSetSizeU
    return pSet
    