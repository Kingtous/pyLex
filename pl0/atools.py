'''
@Author: Kingtous
@Date: 2019-11-01 19:50:57
@LastEditors: Kingtous
@LastEditTime: 2019-11-03 08:23:44
@Description: Kingtous' Code
'''
from parser import Parser
import constDef,atools,sys

def encode(txt):
    return txt.replace("(","{").replace(")","}").replace("*","^")

def decode(txt):
    return txt.replace("{","(").replace("}",")").replace("^","*")

def findSpeNodeInGraph(graph,typecolor):
    for node in graph.nodes:
        if graph.node[node]['color']==typecolor:
            return node

def findAllSpeNodeInGraph(graph,typecolor):
    nodes = []
    for node in graph.nodes:
        if graph.node[node]['color']==typecolor:
            nodes.append(node)
    return nodes

####Parser 区####
parser = None

def initParser(confPath):
    global parser
    # 设置好配置
    parser = Parser(confPath)

def parseOutput(path,txt):
    global parser
    if parser == None:
        initParser(path)
    # 先按 \n 和空格 切片
    mInput = atools.encode(txt).split('\n')
    for i in range(len(mInput)):
        slices = mInput[i].split()
        for sce in slices:
            (return_code,err_str,msg) = parser.parse(parser.getInitDFAStatusBundle(sce))
            if return_code != 0 :
                sys.stderr.write("*"*20+"\n错误号"+str(return_code)+":在第"+str(int(i)+1)+"行,错误位置为：\n>>..."+atools.decode(err_str)+"\n"+msg+"\n"+"*"*20+"\n")
