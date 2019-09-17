"此程序将消除了左递归的三形文法从NFA转化为最小DFA"
import networkx as nx

def convert2NFA(g):
    _startNode = None
    _endNode = None

    cg = nx.MultiDiGraph()
    # 1. 找到起始和终止点，对应red和green

    # 2. 开始迭代

    # 3. 生成dot并且生成pdf
    return cg



if __name__ == "__main__":
    g = nx.nx_pydot.read_dot('test.dot')
    cg = convert2NFA(g)
    pass



