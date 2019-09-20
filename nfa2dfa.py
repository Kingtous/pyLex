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

    cg = nx.MultiDiGraph()
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
    # 2. 开始迭代
    Istruct = dstruct.IclosureStruct(_startNode,tools.expandEpsilonForGraph(g,set([_startNode])).union({_startNode}))
    Iq = queue.Queue()
    Iq.put(Istruct)
    recordList = []
    recordDict = {} # set -> id
    resultIstructDict = dict()

    while not Iq.empty():
        # 取出一个s
        qs = Iq.get()
        # 按照label方向扩展，组成新的几个集合
        for p in range(len(label_list)):
            exp_set = tools.expandMoveForGraph(g,qs.ms,label_list[p])
            exp_set = exp_set.union(tools.expandEpsilonForGraph(g,exp_set))
            try:
                if len(exp_set)!=0:
                    i = recordList.index(exp_set)
                    qs.sDict[label_list[p]]=recordDict[tuple(exp_set)]
                    continue
                continue
            except ValueError:
                newIstruct = dstruct.IclosureStruct(constDef.getAlignName(),exp_set)
                # 不含有，继续命名
                recordList.append(exp_set)
                recordDict[tuple(newIstruct.ms)]=newIstruct.id
                Iq.put(newIstruct)
                qs.sDict[label_list[p]]=newIstruct.id

        resultIstructDict[qs.id]=qs
        # 将集合进行查重，重复的扔掉，没重复的保留，并命名为A,B,C...
    
        
        # 如果有endNode的话，则判断多少结点里面有endNode,将大结点标为endNode

        # 分析保留集合，连接边
        pass
    # 3. 生成dot并且生成pdf
    return cg



if __name__ == "__main__":
    g = nx.nx_pydot.read_dot('lex/test.dot')
    cg = convert2NFA(g)
    pass



