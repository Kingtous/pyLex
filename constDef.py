"""
特殊边
"""
# epsilon
eps = 'eps'
# color
color_startNode = 'red'
color_endNode = 'green'
# none
ver_none = 'none'
prop_label = 'label'
# align name
align_name = '1000'

def getAlignName():
    global align_name
    r = align_name
    align_name = str(int(align_name)+1)
    return r


"""
结点属性为10000+
"""
START_NODE = 10000
EXIT_NODE = 10001

import copy,queue

Iqueue = queue.Queue()

        
