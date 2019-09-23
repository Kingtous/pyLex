"""
Author: Kingtous
Date : 2019/09/24
"""
# 临时构造一个可用的DFA, eps 表示 epsilon, color = red为起始结点, color = green 为终止结点
import networkx as nx
import tools,constDef

def graphDef(mdgraph):
    node_list = ['i','1','2','3','4','5','6','f']
    edge_list = [('i',constDef.eps,'1'),('1','a','1'),('1','b','1'),('1',constDef.eps,'2'),
    ('2','a','3'),('3','a','5'),('2','b','4'),('4','b','5'),('5',constDef.eps,'6'),
    ('6','a','6'),('6','b','6'),('6',constDef.eps,'f')
    ]
    mdgraph.add_nodes_from(node_list)
    tools.addEdgesToGraph(mdgraph,edge_list)
    mdgraph.node['i']['color']=constDef.color_startNode
    mdgraph.node['f']['color']=constDef.color_endNode
    pass


if __name__ == "__main__":
    mdgraph = nx.MultiDiGraph()
    graphDef(mdgraph)
    tools.writeGraph2File(mdgraph,'test.dot')
    tools.convertGraphFile2PDF('test.dot','test.pdf')
    pass