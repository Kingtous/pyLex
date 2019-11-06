'''
@Author: Kingtous
@Date: 2019-11-01 18:40:29
@LastEditors: Kingtous
@LastEditTime: 2019-11-06 19:47:42
@Description: Kingtous' Code
'''
"""
Author: Kingtous
Date : 2019/09/24
"""
import nfa2dfa as DFATool
import reg2nfa as REGTool
import sys,os,networkx as nx
import tools,constDef

# 因为字符中(,),*跟词法里面的(,),*有冲突，我们需要先将源代码里的
# ()分别替换为{}
# * 替换为 ^

rule_sub_str='(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)*(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
rule_str = rule_sub_str + '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|0|1|2|3|4|5|6|7|8|9)*'
rule_bound=',|.|;|{|}'
rule_cal = '+|-|^|/|:=|<|<=|>|>=|#|='
rule_num = '(0|1|2|3|4|5|6|7|8|9)*(0|1|2|3|4|5|6|7|8|9)'
rule_critical = 'begin|call|const|do|end|if|odd|procedure|read|then|var|while|write'
# [标识符，无符号整数，关键字，运算符，分隔符]
rules = [rule_str,rule_num,rule_critical,rule_cal,rule_bound]

if __name__ == "__main__":
    g = []
    for i in range(len(rules)):
        mg = DFATool.convert2NFA(REGTool.genNFA(rules[i]))
        name = tools.findSpeNodeInGraph(mg,constDef.color_startNode)
        mg.node[name]['label'] = str(i)+'_'+ name
        g.append(mg)
    totalGraph = nx.compose_all(g)
    tools.writeGraph2File(totalGraph,"pl0/dfa.dot")
    # dot图生成时如果有,会出现问题，应该把,改为","
    f = open('pl0/dfa.dot')
    content = f.read()
    f.close()
    f=open('pl0/dfa.dot','w')
    content = content.replace("=,",'=","')
    f.write(content)
    f.close()


        


