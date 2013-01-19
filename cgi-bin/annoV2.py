# -*- coding: UTF-8 -*-
#!/usr/bin/python 
 
import re
import cgi 
import os
import itertools
import operator

def parsing(dirname, filename):
    filepath ='data/%s/%s' % (dirname, filename)

    with open(filepath) as f:
        lines = re.findall(r'<s>.*?</s>', f.read())
        lines = [line[3:-4] for line in lines]
        return lines

def display(Content):
    print Content 

def logText(Content):
    print #Content

def myEncoding(text, enfrom, ento): 
    if text:
        return text.decode(enfrom).encode(ento)
    return text

def checkfile(dirname, filename):
    filelist = []
    for fileInfo in os.walk('./data/%s/' % dirname):  
        for fname in fileInfo[2]:  
            if fname[-3:]=='txt' or fname[-3:]=='xml':
                filelist.append(fname)
                
    prevfilename = ''
    nextfilename = ''
    error = None
    
    if not filelist:
        error = 'there is no file in % s folder' % myEncoding(dirname, 'cp949', 'utf-8')
        return filename, prevfilename, nextfilename, error
    
    if not filename:
        filename = filelist[0]
    
    if not filename in filelist:
        error = 'there is no such file (%s)' % myEncoding(filename, 'cp949', 'utf-8')
        return filename, prevfilename, nextfilename, error
            
    fileidx = filelist.index(filename)
    
    if len(filelist) == fileidx+1:
        prevfilename = filelist[fileidx-1]
    elif fileidx == 0:
        nextfilename = filelist[fileidx+1]
    else:
        prevfilename = filelist[fileidx-1]
        nextfilename = filelist[fileidx+1]
    
    return filename, prevfilename, nextfilename, error
                
def displayForm(dirname, filename):
    dirname = myEncoding(dirname, 'utf-8', 'cp949')
    filename = myEncoding(filename, 'utf-8', 'cp949')

    filename, prevfilename, nextfilename, error = checkfile(dirname, filename)
    
    if error:
        display(error)
        return
    
#    logText("display form (" + ' ' + dirname + ' ' + filename + ' ' + nextfilename + ")")
    
    lines = parsing(dirname, filename)
    
    results = []
    try:
        isNoClause = True
        with open('result/%s/Temp%s' % (dirname, filename), 'r') as f:
            annos = re.findall(r"<s>.*?</s>", f.read(), re.DOTALL)
            p = re.compile('<from>(.*?)</from>.*?<to>(.*?)</to>.*?<type>(.*?)</type>.*?<adinfo>(.*?)</adinfo>.*?<comment>(.*?)</comment>', re.DOTALL)
            for anno in annos:
                clauses = re.findall(r'<clause>.*?</clause>', anno, re.DOTALL)
                clauseList = []
                for clause in clauses:
                    isNoClause = False
                    sames = re.findall(r'<same>.*?</same>', clause, re.DOTALL)
                    sames = [list(p.search(same).groups()) for same in sames]
                    clauseList.append(sames)
                results.append(clauseList)
                
            if isNoClause:
                results = []
            
    except Exception as e:
        print 
    
    filename = myEncoding(filename, 'cp949', 'utf-8')
    dirname = myEncoding(dirname, 'cp949', 'utf-8')
    prevfilename = myEncoding(prevfilename, 'cp949', 'utf-8')
    nextfilename = myEncoding(nextfilename, 'cp949', 'utf-8')
    
    HTML = '''
                <form method='post' action='annoV2.py'>
                <input type=hidden name='dirname' value='%s'/>
                <input type=hidden name='filename' value='%s'/>
                <input type=hidden name='prev' value='%s'/>
                <input type=hidden name='next' value='%s'/>
            ''' % (dirname, filename, prevfilename, nextfilename)
            
    HTML += open('html/scriptV2.js').read() + 'FILENAME : %s' % filename
    
    idx = 0
    uniqueId = 0
    for line in lines:
        words = line.split()
        
        tableHTML = "<hr/><br/><div name='div%d'><nobr>%d) %s</nobr><br/><br/><table name='table%s' border='1'><tr>" % (idx, idx+1, line, idx)
        for word in words:
            tableHTML += "<td nowrap=true name='td%d'>" % idx + word + "</td>"
        tableHTML += "</tr><tr align='center'>"
        for i in range(len(words)):
            tableHTML += "<td><input type='checkbox' name='check%d' value='%d'></td>" % (idx, i) 
        tableHTML += "</tr></table><br/>"
        
        typelist = ('명사절','부사절','인용절','관형사절-동격','관형사절-동격-의존명사','관형사절-관계-주격', '관형사절-관계-목적격', '관형사절-관계-부사격', 'Unknown')

        selectHTML = '''<table><tr><td>Type<td/>
                        <select name ='select%d' size='1'>
                        <option value='0' selected>%s</option>
                        <option value='1'>%s</option>
                        <option value='2'>%s</option>
                        <option value='3'>%s</option>
                        <option value='4'>%s</option>
                        <option value='5'>%s</option>
                        <option value='6'>%s</option>
                        <option value='7'>%s</option>
                        <option value='8'>%s</option>
                        </select>
                        </tr>
                    ''' % ((idx,)+typelist)
        selectHTML += '''<tr><td>
                        Additinal Info</td><td>
                        <input type='text' name ='adinfo%d' size='100'/>
                        </td></tr>
                        ''' % idx
        selectHTML += '''<tr><td>Comment
                        </td><td>
                        <input type='text' name ='comment%d' size='100'/>
                        </td></tr>
                        </table>
                        ''' % idx
                        
        addHTML = '''<input type='button' value='Add New Clause' onClick='addNewClause(%d)'>
                     <input type='button' value='Delete All Clauses' onclick='deleteAllClauses(%d)'/>
                    ''' % (idx, idx)
        
        clauseHTML = ""
        if results:
            clauseHTML = "<div name='clauseInfoDiv%d'>" % idx
            clauseHTML += '''<input type='hidden' name='nClause%d' value='%d'/>
                             <br/>
                          ''' % (idx, len(results[idx]))
            
            for sames in results[idx]:
                clauseHTML += '''<div name='clauseInfos%d' id='clauseInfos%d' style="border:1px solid;"><input type='hidden' name='clauseValue%d' value='%d'/>
                                <input type='button' value='Add Clause' onclick='addClause(%d, %d)'/>
                                <br/>''' % (idx, uniqueId, idx, len(sames), idx, uniqueId)
                uniqueId += 1           
                     
                for same in sames:
                    textStr = " ".join(words[int(same[0]):int(same[1])+1])
                    textStr += " - (%s, %s)" % (typelist[int(same[2])], same[3])
                    clauseHTML += '''
                        <div id='clauseInfo%d'>
                        <input type='text' size='%d' onmouseout='highlightBack(%d,%d,%d)' onmouseover='highlight(%d,%d,%d)' value='%s'/>
                        <input type='hidden' name='clauseValue%d' value='%s'/>
                        <input type='hidden' name='clauseValue%d' value='%s'/>
                        <input type='hidden' name='clauseValue%d' value='%s'/>
                        <input type='hidden' name='clauseValue%d' value='%s'/>
                        <input type='hidden' name='clauseValue%d' value='%s'/>
                        <input type='button' value='Delete Clause' onclick='deleteClause(%d, %d)'/>
                        </div>
                        ''' % ((uniqueId, int(len(textStr))) + (idx, int(same[0]), int(same[1]))*2 + (textStr,) + reduce(operator.add, tuple(zip((idx,)*5,tuple(same)))) + (idx, uniqueId,)) 
                    uniqueId += 1
                clauseHTML += "</div><br/>"
            clauseHTML += "</div>"
        else:
            clauseHTML = "<div name='clauseInfoDiv%d'>" % idx
            clauseHTML += '''<input type='hidden' name='nClause%d' value='%d'/>
                             <br/></div>
                          ''' % (idx, 0)
            
        HTML += tableHTML + selectHTML + addHTML + clauseHTML + "</div><br/><br/>"

        idx += 1
    
    prevdisabled = ''
    nextdisabled = ''
    
    if prevfilename == '':
        prevdisabled = 'disabled'
    if nextfilename == '':
        nextdisabled = 'disabled'
    
    HTML += '''    <input type='hidden' name='nSentence' value='%d'/>
                   <input type='submit' name='submitprev' value='prev' %s/>
                   <input type='submit' name='submitnext' value='next' %s/>
               </form><Script Type='text/javascript'>uniqueId=%d</script>
            ''' % (len(lines), prevdisabled, nextdisabled, uniqueId)

    display(HTML) 

def indexForm():
    HTML = '''<form method='post' action='annoV2.py'>
                Directory Name
                <input type=hidden name='init' value='init'/>
                <input type='text' name='dirname' value=""/> 
                File Name
                <input type='text' name='filename' value=""/>
                <input type='submit' value='start'>
              </form>
            '''
    display(HTML)

def saveAnnotation(form, dirname, filename):
    logData = ""
    
    for i in range(int(form.getvalue('nSentence'))):
        logData += "<s>"
        if int(form.getvalue('nClause%d' % i)) > 0:
            values = form.getvalue('clauseValue%d' % i)
            
            idx = 0
            nClause = 0
            isFirst = True
            while nClause < int(form.getvalue('nClause%d' % i)):
                if isFirst:
                    logData += '\n'
                    isFirst = False 
                logData += "\t<clause>\n"
                nSames = int(values[idx])
                for j in range(nSames):
                    logData += "\t\t<same>\n"
                    logData += '''\t\t\t<from>%s</from>\n\t\t\t<to>%s</to>\n\t\t\t<type>%s</type>\n\t\t\t<adinfo>%s</adinfo>\n\t\t\t<comment>%s</comment>\n''' % tuple(values[idx+1:idx+6])
                    logData += "\t\t</same>\n"
                    idx += 5
                idx += 1
                nClause += 1
                logData += "\t</clause>\n"
        logData += "</s>\n"
    
    filename = myEncoding(filename,'utf-8','cp949')
    dirname = myEncoding(dirname,'utf-8','cp949')
    
    open('result/%s/%s' % (dirname, filename), 'w+').write(logData)
    
def main():  
    display("Content-Type: text/html; charset-UTF-8\n\n")
    display("<html><head><title>Sentence annotator</title></head><body>")
    
    form = cgi.FieldStorage() 
    
    try:
        form['init'].value
        try:
            dirname = form['dirname'].value
            filename = form.getvalue('filename')
            
            displayForm(dirname, filename)
        except KeyError:
            display('input folder name')
                
    except KeyError:
        try:
            dirname = form['dirname'].value
            
            filename = form.getvalue('filename')
            prevfilename = form.getvalue('prev')
            nextfilename = form.getvalue('next')
            
            if form.getvalue('submitprev'):
                saveAnnotation(form, dirname, filename)
                displayForm(dirname, prevfilename)
            else:
                saveAnnotation(form, dirname, filename)
                displayForm(dirname, nextfilename)
                
        except KeyError:
            indexForm()
            
    display('</body></html>')
            
if __name__ == '__main__':
    main()
