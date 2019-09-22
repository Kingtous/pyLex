"""
特殊边
"""
# epsilon
eps = 'eps'
# color
color_normal = 'black'
color_startNode = 'red'
color_endNode = 'green'
# none
ver_none = 'none'
prop_label = 'label'
# align name
align_name = 'A'
# node kind
nodeLabel = 'COMMON_NODE'
startNodeLabel = 'START_NODE'
endNodeLabel = 'END_NODE'
# Dict Default
noneKey = 'NONE'
label2colorDict = {nodeLabel:color_normal,startNodeLabel:color_startNode,endNodeLabel:color_endNode}

def getAlignName():
    global align_name
    r = align_name
    align_name = chr(ord(align_name)+1)
    return r

"""
结点属性为10000+
"""
START_NODE = 10000
EXIT_NODE = 10001

import copy,queue

Iqueue = queue.Queue()

        
