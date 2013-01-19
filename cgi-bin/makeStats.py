# -*- coding: UTF-8 -*-

import os
import re

filelist = []
for fileInfo in os.walk('../statdata/'):  
    for fname in fileInfo[2]:  
        if fname[-3:]=='txt' or fname[-3:]=='xml':
            fullpath = os.path.join(fileInfo[0], fname)
            filelist.append(fullpath)
            
rSen = re.compile(r'<s.*?>(.*?)</s>', re.DOTALL)
nFile = 0
nSentence = 0
nClause = 0

p = re.compile('<same>.*?<from>(.*?)</from>.*?<to>(.*?)</to>.*?<type>(.*?)</type>.*?<adinfo>(.*?)</adinfo>.*?<comment>(.*?)</comment>.*?</same>', re.DOTALL)

with open('../statistic.txt', 'w') as sf:
    for filename in filelist:
        print filename.decode('euc-kr').encode('utf-8')
        
        with open('../statdata/%s' % filename, 'r') as f:
            sentences = re.findall(r"<s>.*?</s>", f.read(), re.DOTALL)
        
        with open(re.sub('statdata', 'data', filename), 'r') as fd:
            lines = re.findall(r"<s>.*?</s>", fd.read(), re.DOTALL)
            lines = [line[3:-4] for line in lines]
        
        idx = 0
        for sentence in sentences:
            clauses = re.findall(r"<clause>.*?</clause>", sentence, re.DOTALL)
            if clauses:
                for clause in clauses:
                    sames = re.findall(r"<same>.*?</same>", clause, re.DOTALL)
                    for same in sames:
                        same = [list(p.search(same).groups()) for same in sames]
                        infos = [filename.decode('euc-kr').encode('utf-8'), lines[idx], nFile, nSentence, nClause]
                        infos.append(same)
                        infos.append('\n')
                        sf.write('\t'.join(['%s' % info for info in infos]))
                    nClause += 1
            else: 
                infos = [filename.decode('euc-kr').encode('utf-8'), lines[idx], nFile, nSentence, '', '', '', '', '', '', '\n']
                sf.write('\t'.join(['%s' % info for info in infos]))
            nSentence += 1
            idx += 1
        nFile += 1
        