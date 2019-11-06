'''
@Author: Kingtous
@Date: 2019-11-01 18:40:29
@LastEditors: Kingtous
@LastEditTime: 2019-11-02 13:05:53
@Description: Kingtous' Code
'''
"""
Author: Kingtous
Date : 2019/09/24
"""
# epsilon
eps = 'eps'
# color
color_normal = 'black'
color_startNode = 'red'
color_endNode = 'green'
# none
ver_none = 'none'
prop_label = 'label'
# align name , BC用来表示起始和终止，所以从C开始
align_name = 'D'
nfa_node_start_name = 'A'
# node kind
nodeLabel = 'COMMON_NODE'
startNodeLabel = 'START_NODE'
endNodeLabel = 'END_NODE'
# Dict Default
noneKey = 'NONE'
DEBUG = True
label2colorDict = {nodeLabel:color_normal,startNodeLabel:color_startNode,endNodeLabel:color_endNode}

def getAlignName():
    global align_name
    r = align_name
    if r[-1] == 'Z':
        r = r + 'A'
    else:
        r = r[:-1] + chr(ord(r[-1])+1)
    align_name = r
    return r

def getNFANodeName():
    global nfa_node_start_name
    r = nfa_node_start_name
    if r[-1] == 'Z':
        r = r + 'A'
    else:
        r = r[:-1] + chr(ord(r[-1])+1)
    nfa_node_start_name = r
    return r

"""
结点属性为10000+
"""
START_NODE = 10000
EXIT_NODE = 10001
        
##
# reg -> nfa const definition
charset = {'|','(',')','*'}

# rules = [rule_str,rule_num,rule_critical,rule_cal,rule_bound]
errmsg =[
    "字符串命名错误，命名规范: 1.只能含有首字母和数字. 2.首字符不能为数字.",
    "数字格式错误，请检查",
    "保留字命名错误，请检查",
    "运算符格式错误，请检查",
    "界符格式错误或未定义错误"
]
