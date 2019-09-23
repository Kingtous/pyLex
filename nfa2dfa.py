"此程序将消除了左递归的三形文法从NFA转化为最小DFA"
import networkx as nx
import constDef,tip,dstruct
import sys,queue,tools

def simplfyDFA(dfa):
    """
    化简一个DFA为最简DFA，直接修改传参
    """

    pass

def convert2NFA(g):
    _startNode = None
    _endNode = None
    _char = 'A'

    # 1. 找到起始和终止点，对应red和green
    for node in g.nodes:
        try:
            if g.node[node]['color']==constDef.color_startNode:
                _startNode = node
            elif g.node[node]['color']==constDef.color_endNode:
                _endNode = node
        except KeyError:
            # 没有Color标签的证明是普通结点
            continue
    if _startNode == None:
        sys.stderr.write(tip.MSG_NO_START_NODE)
        exit(-1)
    # 2. 获取边的label情况
    labels = nx.get_edge_attributes(g,'label')
    label_set = set()
    for item in labels.items():
        label_set.add(item[1])
    label_list = list(label_set)
    try:
        label_list.remove(constDef.eps)
    except ValueError:
        pass
    # 3. 开始迭代
    Istruct = dstruct.IclosureStruct(_startNode,tools.expandEpsilonForGraph(g,set([_startNode])).union({_startNode}))
    Iq = queue.Queue()
    Iq.put(Istruct)

    # 变量定义
    recordList = list()
    recordDict = dict() # set -> id
    resultIstructDict = dict()
    setList = list()

    while not Iq.empty():
        # 取出一个s
        qs = Iq.get()
        # 按照label方向扩展，组成新的几个集合
        for p in range(len(label_list)):
            exp_set = tools.expandMoveForGraph(g,qs.ms,label_list[p])
            exp_set = exp_set.union(tools.expandEpsilonForGraph(g,exp_set))
            try:
                if len(exp_set)!=0:
                    recordList.index(exp_set)
                    # 增加对应的ID
                    qs.sDict[label_list[p]]=recordDict[tuple(exp_set)]
                    continue
                continue
            except ValueError:
                # 准备添加新结点，先确定结点类型
                # 添加结点
                newIstruct = dstruct.IclosureStruct(constDef.getAlignName(),exp_set)
                # 不含有，继续命名
                recordList.append(exp_set)
                recordDict[tuple(newIstruct.ms)]=newIstruct.id
                Iq.put(newIstruct)
                qs.sDict[label_list[p]]=newIstruct.id
        resultIstructDict[qs.id]=qs
    # 添加start和end结点，以及构造后面要用的setList
    endSet = set()
    startSet = set()
    for rIstruct in resultIstructDict.items():
        qs = rIstruct[1]
        if _startNode in qs.ms:
            qs.node = constDef.startNodeLabel
        elif _endNode in qs.ms:
            qs.node = constDef.endNodeLabel
            endSet.add(qs.id)
            continue
        startSet.add(qs.id)
    setList = [startSet,endSet]
    # 构造新的确定DFA
    cg = nx.MultiDiGraph()
    # 第一遍：添加结点
    for rIi in resultIstructDict.items():
        rI = rIi[1]
        color = constDef.label2colorDict[rI.node]
        cg.add_node(rI.id,color=color)
    # 第二遍：添加边
    for rIi in resultIstructDict.items():
        rI = rIi[1]
        for label in rI.sDict.keys():
            cg.add_edge(rI.id,rI.sDict[label],label=label,key=label)
    # 化简确定的DFA
    tools.simplifyDFA(cg,setList,label_list)
    return cg


def genSimplifiedDFA(nfaDotPath):
    return convert2NFA(nx.nx_pydot.read_dot(nfaDotPath))


if __name__ == "__main__":
    g = nx.nx_pydot.read_dot('lex/test_2.dot')
    cg = convert2NFA(g)
    # 生成dot并且生成pdf
    nx.nx_pydot.write_dot(cg,'lex/result.dot')
    pass



