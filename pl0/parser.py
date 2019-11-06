'''
@Author: Kingtous
@Date: 2019-11-01 20:02:51
@LastEditors: Kingtous
@LastEditTime: 2019-11-02 13:03:51
@Description: Kingtous' Code
'''
import networkx as nx
import atools,constDef


class DFAStatus:
    # 用来存储当前输入字符串输入DFA的哪个状态
    def __init__(self,totalStr,startPos,aPos):
        self.startPos = startPos # start position:起始位置
        self.aPos =  aPos # analyze position:当前分析到的字符串的位置
        self.totalStr = totalStr 
        self.status = list()

    def getSubStr(self):
        return self.totalStr[self.startPos:self.aPos]
    
    def symStartPos(self):
        self.startPos = self.aPos

    def addStatus(self,dfaID,nodename):
        self.status.append([dfaID,nodename])
    
    def isEmpty(self):
        return len(self.status) == 0
    
    def isEnd(self):
        return self.aPos >= len(self.totalStr)

    def moveToNext(self):
        if self.aPos + 1 >= len(self.totalStr):
            return False
        else:
            self.aPos = self.aPos + 1
            return True
    
    def setStatus(self,status):
        self.status = status

    def getStatus(self):
        return self.status

    def getCurrentCh(self):
        c = self.totalStr[self.aPos]
        if not c.isalnum():
            # Graphviz 对特殊字符处理会多加双引号
            c = '"'+c+'"'
        return c

    def getStr(self):
        return self.totalStr
        

class Parser:

    def __init__(self,path):
        # multidigraph
        self.g = nx.nx_pydot.read_dot(path)
        # 输出为二元组
        self.output = []
        self.startNodes = atools.findAllSpeNodeInGraph(self.g,constDef.color_startNode)
        self.endNodes = atools.findAllSpeNodeInGraph(self.g,constDef.color_endNode)

    def parse(self,dfaStatus):
        # point 指向下一个判断的单词
        # 返回下一个字符是否属于该DFA,如果属于拓展过去，如果不属于则判断currentStep中是否已经处于终止(绿色)结点
        # 返回：dfaStatus

        while not dfaStatus.isEnd():
            cStatus = dfaStatus.getStatus()
            totalStr = dfaStatus.getStr()
            # 临时变量
            newStatus = []
            newOutputBuffer = []
            errFlag = -1
            # 遍历 DFA
            for dfa in cStatus:
                # dfa格式：(dfa的ID, 当前结点的名字)
                flag = False
                for nei in nx.neighbors(self.g,dfa[1]):
                    # 检查相邻边
                    c = dfaStatus.getCurrentCh() # 取出当前要处理的字符
                    if self.g.has_edge(dfa[1],nei,key=c):
                        # 如果当前DFA可以接受这个字符
                        newStatus.append([dfa[0],nei])
                        flag = True
                        # DFA一次只会出现一个可接受的情况，直接break
                        break
                    else:
                        continue
                # 没有这条边，判断是否已经为终止结点
                if flag == False:
                    # 当前DFA不能接受该字符
                    # vara
                    if dfa[1] in self.endNodes:
                        # 已经为终止结点,证明前面的已经为一个可规约的字符串，先保存到缓存中(特判保留字和字符串)
                        newOutputBuffer.append([dfa[0],dfaStatus.getSubStr()])
                    else:
                        # 不是终止结点，则把当前错误ID定为DFA的ID号
                        errFlag = dfa[0]
            
            # 针对outputbuffer大于1的时候的特判
            if len(newOutputBuffer)>1:
                # 下一个已经是不能识别的符号，而前面的都属于：特判字符串、保留字，转为保留字，此处保留字为'2'
                self.output.append(['2',newOutputBuffer[0][1]])
                if constDef.DEBUG:
                    self.output[-1][1]=atools.decode(self.output[-1][1])
                    print(self.output[-1])
                dfaStatus.symStartPos()
                dfaStatus.setStatus(self.getInitDFAStatus())
                continue
            elif len(newOutputBuffer) == 1:
                # 输出了，return 新的status
                # TODO vara这种情况可能还要特判，因为此时为，非保留字且status中有字符串
                if newOutputBuffer[0][0]=='2':
                    # 如果 newStatus 中有识别为字符串的，则不识别为保留字，识别为字符串，即不刷新buffer
                    hasStr = False
                    for it in newStatus:
                        if it[0] == '0':
                            hasStr = True
                            break
                    if hasStr:
                        newOutputBuffer.clear()
                        dfaStatus.setStatus(newStatus)
                        if not dfaStatus.moveToNext():
                            return (0,0,"")
                        continue
                    else:
                        pass
                # newOutputBuffer 只有一个

                # 特判：输入数字后的那个字符不能为字母
                if newOutputBuffer[0][0]=='1' and  dfaStatus.getCurrentCh().isalpha():
                    # 报错
                    return (int(newOutputBuffer[0][0]),totalStr[dfaStatus.startPos:],constDef.errmsg[int(newOutputBuffer[0][0])])

                self.output = self.output + newOutputBuffer
                if constDef.DEBUG:
                    newOutputBuffer[0][1]=atools.decode(newOutputBuffer[0][1])
                    print(newOutputBuffer[0])
                dfaStatus.symStartPos()
                dfaStatus.setStatus(self.getInitDFAStatus())
                continue
            else:
                # 还没到底
                if int(errFlag) != -1 and len(newStatus)==0:
                    return (int(errFlag),totalStr[dfaStatus.startPos:],constDef.errmsg[int(errFlag)])
                dfaStatus.setStatus(newStatus)
                if not dfaStatus.moveToNext():
                    # 走到尽头,选择第一个符合条件的
                    if len(newStatus)==2:
                        # 特判保留字和字符串
                        self.output.append(['2',dfaStatus.getStr()[dfaStatus.startPos:]])
                    else:
                        self.output.append([newStatus[0][0],dfaStatus.getStr()[dfaStatus.startPos:]])
                    if constDef.DEBUG:
                        self.output[-1][1]=atools.decode(self.output[-1][1])
                        print(self.output[-1])
                    return (0,0,"")

    def getInitDFAStatusBundle(self,txt,spos=0,apos=0):
        status = DFAStatus(txt,spos,apos)
        for n in self.startNodes:
            # 注意： startNodes的label才含标签
            status.addStatus(self.g.node[n]['label'].replace('"','').split('_')[0],n)
        return status

    def getInitDFAStatus(self):
        slist = []
        for n in self.startNodes:
            # 注意： startNodes的label才含标签
            slist.append([self.g.node[n]['label'].replace('"','').split('_')[0],n])
        return slist
