"""
特殊边
"""
# epsilon
eps = 'eps'

"""
结点属性为10000+
"""
START_NODE = 10000
EXIT_NODE = 10001

import copy,queue

Iqueue = queue.Queue()

class IclosureStruct:
    def __init__(self,id,selectedSet):
        self.id = id
        self.ss = selectedSet
        self.ls = None
        self.rs = None
        
