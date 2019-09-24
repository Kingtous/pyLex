"""
Author: Kingtous
Date : 2019/09/24
"""
import networkx as nx
import tools

# 特殊符号： |,(,),*
ch_set = {}

test_str_1 = '1(1010*|1(010)*1)*0'
test_str_2 = '(a(a*b)(a|b))*a*(a|(b|a))b'
test_str_3 = 'c(a|bc*)*(a)'
test_str_4 = 'a*b|b*a|(a|b)*a*'

def genNFA(s):
    # 建立多向图
    g = nx.MultiDiGraph()
    # 建立起始结点和终止结点
    _startNode = tools.claimChar()
    _endNode = tools.claimChar()
    g.add_node(_startNode,color='red')
    g.add_node(_endNode,color ='green')
    # 开始处理正则式
    tools.parseStatement(g,s,_startNode,_endNode)
    return g

if __name__ == "__main__":
    nx.nx_pydot.write_dot(genNFA(test_str_1),'nfa.dot')
   
    