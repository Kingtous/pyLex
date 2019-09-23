import networkx as nx
import tools

# 特殊符号： |,(,),*
ch_set = {}

test_str = 'c(a|bc*)*(a)'
back_str = 'a*b|b*a|(a|b)*a*'
simple_str = '1(1010*|1(010)*1)*0'

def genNFA():
    # 建立多向图
    g = nx.MultiDiGraph()
    # 建立起始结点和终止结点
    _startNode = tools.claimChar()
    _endNode = tools.claimChar()
    g.add_node(_startNode,color='red')
    g.add_node(_endNode,color ='green')
    # 开始处理正则式
    tools.parseStatement(g,simple_str,_startNode,_endNode)
    return g

if __name__ == "__main__":
    nx.nx_pydot.write_dot(genNFA(),'lex/nfa.dot')
   
    