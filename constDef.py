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
# align name , BC用来表示起始和终止，所以从C开始
align_name = 'D'
nfa_node_start_name = 'A'
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
    if r[-1] == 'Z':
        r = r + 'A'
    else:
        r = r[:-1] + chr(ord(r[-1])+1)
    align_name = r
    return r

def getNFANodeName():
    global nfa_node_start_name
    r = nfa_node_start_name
    if r[-1] == 'Z':
        r = r + 'A'
    else:
        r = r[:-1] + chr(ord(r[-1])+1)
    nfa_node_start_name = r
    return r

"""
结点属性为10000+
"""
START_NODE = 10000
EXIT_NODE = 10001
        
##
# reg -> nfa const definition
charset = {'|','(',')','*'}
