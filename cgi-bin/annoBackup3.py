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

def checkfile(dirname, filename):
    filelist = []
    for fileInfo in os.walk('./data/%s/' % dirname):  
        for fname in fileInfo[2]:  
            if fname[-3:]=='txt' or fname[-3:]=='xml':
                filelist.append(fname)
    
    if not filelist:
        return filename, None
    
    if filename == '':
        filename = filelist[0]
        
    if not filename in filelist:
        return filename, None
            
    fileidx = filelist.index(filename)
    if len(filelist) == fileidx+1:
        return filename, 'EOF'
    else:
        return filename, filelist[fileidx+1]
                
def displayForm(dirname, filename):
    dirname = dirname.decode('utf-8').encode('cp949')
    filename = filename.decode('utf-8').encode('cp949')
    
    filename, nextfilename = checkfile(dirname, filename) 
    if not nextfilename:
        display("There is no such file")
        return
    
    logText("display form (" + ' ' + dirname + ' ' + filename + ' ' + nextfilename + ")")
    lines = parsing(dirname, filename)
    
    filename = filename.decode('cp949').encode('utf-8')
    dirname = dirname.decode('cp949').encode('utf-8')
    nextfilename = nextfilename.decode('cp949').encode('utf-8') 
    
    HTML = "<form method='post' action='anno.py'><input type=hidden name='before' value='"+filename+"'><input type=hidden name='dirname' value='"+dirname+"'><input type=hidden name='filename' value='"+nextfilename+"'/>"
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
        
        selectHTML = '''Type <select name ='select%d' size='1'>
                        <option value='0' selected>%s</option>
                        <option value='1'>%s</option>
                        <option value='2'>%s</option>
                        <option value='3'>%s</option>
                        <option value='4'>%s</option>
                        <option value='5'>%s</option>
                        <option value='6'>%s</option>
                        <option value='7'>%s</option>
                        </select>
                    ''' % (idx, '명사절','부사절','인용절','관형사절-동격','관형사절-동격-의존명사','관형사절-관계-주격', '관형사절-관계-목적격', '관형사절-관계-부사격')
        
        addHTML = "<input type='button' value='Add' onClick='addClause(%d)'><br/></div>" % idx
        
        textHTML = "<input type=hidden name='isClause%d' value='isClause'/><input type=hidden name='clause%d' value=''/>" % (idx, idx)
        
        HTML += tableHTML + selectHTML + addHTML + textHTML + "<br/><br/>"
        
        idx += 1
    HTML += "<input type='submit' value='submit'></form>"        
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
    
    filename = filename.decode('utf-8').encode('cp949')
    dirname = dirname.decode('utf-8').encode('cp949')
    
    open('result/%s/%s' % (dirname, filename), 'w+').write(logData)
    
def main():  
    display("Content-Type: text/html; charset-UTF-8\n\n")
    display("<html><head><title>Sentence annotator</title></head><body>")
    
    form = cgi.FieldStorage() 
    
    try:
        form['init'].value
        try:
            dirname = form['dirname'].value
        except KeyError:
            dirname = ''
        
        try:
            filename = form['filename'].value
        except KeyError:
            filename = ''
            
        displayForm(dirname, filename)
    except KeyError:
        try:
            dirname = form['dirname'].value
            if not form.getvalue('filename'):
                filename = ''
            else:
                filename = form['filename'].value
            
            before = form['before'].value
            
            saveAnnotation(form, dirname, before)
            if filename == 'EOF':
                display('Annotation Complete in %s Directory' % dirname)
            else:
                displayForm(dirname, filename)
        except KeyError:
            indexForm()
            
    display('</body></html>')
            
if __name__ == '__main__':
    main()
