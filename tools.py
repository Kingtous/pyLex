import networkx as nx
import constDef

def writeGraph2File(multidigraph,filePath):
    nx.nx_pydot.write_dot(multidigraph,filePath)

def convertGraphFile2PDF(filePath,pdfName):
    import os
    if not os.path.exists(filePath):
        return False
    os.system('dot -Tpdf '+filePath+' -o'+pdfName)

def addEdgesToGraph(multidigraph,lis):
    for tri_arr in lis:
        multidigraph.add_edge(tri_arr[0],tri_arr[2],label=tri_arr[1])

def expandMoveForGraph(multidigraph,oriSet,dir):
    """
    multidigraph : graph
    oriSet : ori Set of vertex
    dir : expand direction
    """
    import copy,constDef
    aSet = set()
    # 求move(I,dir)
    for vertex in oriSet:
        for nei in nx.neighbors(multidigraph,vertex):
            edata = multidigraph.get_edge_data(vertex,nei) # dict
            for ekey in edata.keys():
                data = edata[ekey]
                fresult = data.get(constDef.prop_label,constDef.ver_none)
                if fresult == constDef.ver_none:
                    import sys
                    sys.stderr.write('No Label From '+vertex+'To'+nei)
                    exit(-1)
                elif fresult == dir:
                    aSet.add(nei)
    return aSet

def expandEpsilonForGraph(multidigraph,oriSet):
    import constDef,copy
    pSet = copy.copy(oriSet)
    pSetSize = len(pSet)
    while True:
        pSet = pSet.union(expandMoveForGraph(multidigraph,pSet,constDef.eps))
        pSetSizeU = len(pSet)
        if pSetSizeU == pSetSize:
            break
        else:
            pSetSize = pSetSizeU
    return pSet

def simplifyDFA(multidigraph,setList,dirList):
    # setList 为初始List，含有两个集合，一个集合存放终止集合，一个存放起始结点和中间结点

    toDict = dict()

    # 重置标志
    oriLen = len(setList)
    Irestart = False

    # 临时变量，用于给简化的内容重新赋值
    compileID = oriLen

    # 构造映射字典(索引)
    for i in range(oriLen):
        for v in setList[i]:
            toDict[v]=i

    while True:
        # 重置标志
        oriLen = len(setList)
        Irestart = False
        for i in range(oriLen):
            # 先按dirList中的一个dir进行拓展
            for dir in dirList:
                new_set_list = classifyMoveSet(multidigraph,setList[i],dir,toDict)
                if len(new_set_list) > 1:
                    # 可划分,则用new_set_list与setList合并，并且删除setList[i]，重新构造字典
                    setList.remove(setList[i])
                    setList = setList + new_set_list
                    for s in new_set_list:
                        # 分组之后，需要更新映射字典
                        compileID = compileID + 1
                        for v in s:
                            toDict[v] = compileID
                    Irestart = True
                    break
                pass
            if Irestart == True:
                break
        if Irestart == True:
            continue
        length = len(setList)
        if length == oriLen:
            break
    # 此时化简完成，开始按照setList进行化简，直接对传值得到的图进行修改操作
    for s in setList:
        if len(s) == 1:
            # 只有一个，不删除
            continue
        # 取其中的第一个元素替换
        s = tuple(s)
        first_v = s[0]
        # 将其他元素的入点指向first_v,出点从first_v指出
        for i in range(1,len(s)):
            # 前驱,后继
            # pre_edges = multidigraph.adj[s[i]]
            # for pe in pre_edges.values():
            #     pass
            # pass
            pres = multidigraph.predecessors(s[i])
            for pre in list(pres):
                for key in dirList:
                    # TODO 还要检查标签，别忘了
                    if multidigraph.has_edge(pre,s[i],key=key) and not multidigraph.has_edge(pre,first_v,key=key):
                        # 加上 pre -> first_v
                        # 删除 pre -> s[i]
                        if pre == s[i]:
                            # 自我循环,加入到first_v -> first_v
                            multidigraph.add_edge(first_v,first_v,key=key,label=key)
                            pass
                        else:
                            multidigraph.add_edge(pre,first_v,key=key,label=key)
                        # TODO 要remove 不同label的而不能全部清空
                        multidigraph.remove_edge(pre,s[i],key=key)
                        pass
            succs = multidigraph.successors(s[i])
            for succ in list(succs):
                for key in dirList:
                    # TODO 还要检查标签，别忘了
                    if multidigraph.has_edge(succ,s[i],key=key) and not multidigraph.has_edge(first_v,succ,key=key):
                        # 加上 first_v -> succ
                        # 删除 s[i] -> succ
                        if pre == s[i]:
                            # 在 pre 中就处理过了，跳过
                            continue
                        else:
                            multidigraph.add_edge(first_v,succ,key=key,label=key)
                        # TODO 要remove 相同label的而不能全部清空
                        multidigraph.remove_edge(s[i],succ,key=key)
                        pass
            multidigraph.remove_node(s[i])
            pass

    pass


def classifyMoveSet(multidigraph,vSet,dir,toDict):
    if len(vSet) == 1 :
        # 只有一个元素
        return vSet
    # 将vSet向dir进行扩展，并进行分组
    t_set_dict = {}
    # t_set_list = [为空，集合1，集合2，集合3...]
    for v in vSet:
        v_t = moveToDir(multidigraph,v,dir)
        if v_t == None:
            if t_set_dict.get(constDef.noneKey,None) == None:
                t_set_dict[constDef.noneKey] = set()
            t_set_dict[constDef.noneKey].add(v)
        else:
            if t_set_dict.get(toDict[v_t],None) == None:
                    t_set_dict[toDict[v_t]] = set()
            t_set_dict[toDict[v_t]].add(v)
    return list(t_set_dict.values())

def moveToDir(multidigraph,vertex,dir):
    tmp_v = None
    neis = nx.neighbors(multidigraph,vertex)
    for nei in neis:
        # 判断是不是这个方向的
        try:
            multidigraph.edges[vertex,nei,dir]['label']
            tmp_v = nei
            break
        except KeyError:
            # 没有dir
            continue
    return tmp_v

def moveToDir_set(multidigraph,vSet,dir):
    tmp_s = set()
    for vertex in vSet:
        neis = nx.neighbors(multidigraph,vertex)
        for nei in neis:
            # 判断是不是这个方向的
            try:
                multidigraph.edges[vertex,nei,dir]['label']
                tmp_s.add(nei)
            except KeyError:
                continue
    return tmp_s
