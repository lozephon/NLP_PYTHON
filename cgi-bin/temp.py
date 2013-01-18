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
nfile = 0
nSentences = 0
nClause = 0

with open('../statistic.txt', 'w') as sf:
    for filename in filelist:
        with open(re.sub('statdata', 'data', filename), 'r') as fd:
            lines = re.findall(r'<s>.*?</s>', fd.read())
            lines = [line[3:-4] for line in lines]
        
        print filename.decode('euc-kr').encode('utf-8')
        with open('../statdata/%s' % filename, 'r') as f:
            sentences = rSen.findall(f.read())
            
            idx = 0
            for sentence in sentences:
                if sentence != '':
                    clauses = sentence.split('/')
                    for clause in clauses:
                        cfrom, cto, rest = clause.split(None, 3)[0:3]
                        ctype, adinfo, comment = rest.split('-')[0:3]

                        infos = [filename.decode('euc-kr').encode('utf-8'), lines[idx], nfile, nSentences, nClause, cfrom, cto, ctype, adinfo, comment, '\n']
                        
                        #print '\t'.join(['%s' % info for info in infos])
                        sf.write('\t'.join(['%s' % info for info in infos]))
                        nClause += 1
                else:
                    infos = [filename.decode('euc-kr').encode('utf-8'), lines[idx], nfile, nSentences, '', '', '', '', '', '', '\n']
                        
                    #print '\t'.join(['%s' % info for info in infos])
                    sf.write('\t'.join(['%s' % info for info in infos]))
                
                idx += 1
                nSentences += 1
            nfile += 1
    
    