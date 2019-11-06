'''
@Author: Kingtous
@Date: 2019-11-01 19:00:59
@LastEditors: Kingtous
@LastEditTime: 2019-11-03 08:55:05
@Description: Kingtous' Code
'''
# pl0 词法分析器
import networkx as nx
import atools
# 调用图生成
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config,GlobbingFilter

confPath = 'dfa.dot'

if __name__ == "__main__":
    f = open('file/1.pl','r')
    mInput = f.read()

    # 生成函数调用图
    graph = GraphvizOutput()
    graph.output_file = 'callgraph.png'
    config = Config(max_depth=4)
    config.trace_filter = GlobbingFilter([
        'atools.*',
        'constDef.*',
        'parser.*'
    ])

    with PyCallGraph(output=graph,config=config):
        atools.parseOutput(confPath,mInput)

