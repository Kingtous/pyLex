"""
Author: Kingtous
Date : 2019/09/24
"""
import nfa2dfa as DFATool
import reg2nfa as REGTool
import sys,os
import tools

if __name__ == "__main__":
    sys.stdout.write('请输入正则式：')
    s = input()
    print('Regular Expression -> Certain DFA...')
    cg = REGTool.genNFA(s)
    print('Certain DFA -> Minimal DFA...')
    mg = DFATool.convert2NFA(cg)
    print('Done.')
    print('Write to Dot File...')
    tools.writeGraph2File(cg,'cg.dot')
    tools.writeGraph2File(mg,'mg.dot')
    print('Converting Dot to PDF...')
    tools.convertGraphFile2PDF('cg.dot','cg.pdf')
    tools.convertGraphFile2PDF('mg.dot','mg.pdf')
    print('Opening PDF File...')
    os.system('qpdfview cg.pdf')
    os.system('qpdfview mg.pdf')


