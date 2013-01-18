# -*- coding: UTF-8 -*-
#!/usr/bin/python 
 
import re
import cgi 
import os

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
    
    filename = myEncoding(filename, 'cp949', 'utf-8')
    dirname = myEncoding(dirname, 'cp949', 'utf-8')
    prevfilename = myEncoding(prevfilename, 'cp949', 'utf-8')
    nextfilename = myEncoding(nextfilename, 'cp949', 'utf-8')
    
    HTML = '''
                <form method='post' action='anno.py'>
                <input type=hidden name='dirname' value='%s'/>
                <input type=hidden name='filename' value='%s'/>
                <input type=hidden name='prev' value='%s'/>
                <input type=hidden name='next' value='%s'/>
            ''' % (dirname, filename, prevfilename, nextfilename)
            
    HTML += open('html/script.js').read()[3:] + 'FILENAME : %s' % filename
    
    idx = 0
    for line in lines:
        words = line.split()
        
        tableHTML = "<hr/><br/><div name='div%d'><nobr>%d) %s</nobr><br/><br/><table name='table%s' border='1'><tr>" % (idx, idx+1, line, idx)
        for word in words:
            tableHTML += "<td nowrap=true name='td%d'>" % idx + word + "</td>"
        tableHTML += "</tr><tr align='center'>"
        for i in range(len(words)):
            tableHTML += "<td><input type='checkbox' name='check%d' value='%d'></td>" % (idx, i) 
        tableHTML += "</tr></table><br/>"
        
        selectHTML = '''<table><tr><td>Type<td/><td><select name ='select%d' size='1'>
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
                        </td></tr>
                    ''' % (idx, '명사절','부사절','인용절','관형사절-동격','관형사절-동격-의존명사','관형사절-관계-주격', '관형사절-관계-목적격', '관형사절-관계-부사격', 'Unknown')
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
                        
        addHTML = "<input type='button' value='Add' onClick='addClause(%d)'><br/></div>" % idx
        
        textHTML = "<input type=hidden name='isClause%d' value='isClause'/><input type=hidden name='clause%d' value=''/>" % (idx, idx)
        
        HTML += tableHTML + selectHTML + addHTML + textHTML + "<br/><br/>"

        idx += 1
    
    prevdisabled = ''
    nextdisabled = ''
    
    if prevfilename == '':
        prevdisabled = 'disabled'
    if nextfilename == '':
        nextdisabled = 'disabled'
    
    HTML += '''    <input type='submit' name='submitprev' value='prev' %s/>
                   <input type='submit' name='submitnext' value='next' %s/>
               </form>
            ''' % (prevdisabled, nextdisabled)

    display(HTML) 

def indexForm():
    HTML = '''<form method='post' action='anno.py'>
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
    
    i = 0
    while form.getvalue('isClause%d' % i):
        clauseStr = ''
        if form.getvalue('clause%d' % i):
            clauseStr = form.getvalue('clause%d' % i)
        logData += '<s num=%d>' % i + clauseStr + '</s>\n'
        i += 1
    
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
