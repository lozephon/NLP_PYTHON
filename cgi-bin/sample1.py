# -*- coding: UTF-8 -*-
#!/usr/bin/python 
 
import re
import cgi 
 
# 틀 파일 이름
TemplateFile = "html/template.html" 
 
# 사용자에게 보여줄 폼 파일 이름
FormFile = "html/form.html" 

# Display 함수.  출력할 문자열인 하나의 인수를 받는다.
def Display(Content):
    TemplateHandle = open(TemplateFile, "r")  # 파일 읽기모드로 오픈
    # 전체 파일을 읽는다
    TemplateInput = TemplateHandle.read()
    TemplateHandle.close()                    # 파일 클로우즈
    # 틀 파일이 잘못 되었을 때의 예외 정의
    BadTemplateException = "HTML 틀 파일에 문제가 생겼어요~" 
 
    SubResult = re.subn("<!-- \*\*\* INSERT CONTENT HERE \*\*\* -->", Content,TemplateInput)
    if SubResult[1] == 0:

        raise BadTemplateException 
    print "Content-Type: text/html\n\n"
    print SubResult[0] 
 
### 틀을 보여주고, 그 것을 처리하는 두 개의 매인 행동 함수 정의
 
# 간단한 함수임.
def DisplayForm():

    FormHandle = open(FormFile, "r")

    FormInput = FormHandle.read()

    FormHandle.close()    
    Display(FormInput) 
 
def ProcessForm(form):    

    # 폼에서 정보를 쉽게 추출..
    try:
        name = form["name"].value
    except:
        Display("이름은 입력하셔야 합니다. 되돌아가 주세요")
        raise SystemExit
    try:
        email = form["email"].value
    except:
        email = None
    try:
        color = form["color"].value
    except:
        color = None
    try:
        comment = form["comment"].value
    except:
        comment = None 
 
    Output = ""  # 출력 버퍼 초기화
    Output = Output + "Hello, "     
 
    if email != None:
        Output = Output + "<A HREF=\"mailto:\"" + email + ">" +  name + "</A>.<P>"
    #else:
        #Output = Output + name + ".<P>"     

    if color == "swallow":
        Output = Output + "You must be a Monty Python fan.<P>"
    elif color != None:
        Output = Output + "Your favorite color was " + color + "<P>"
    else:
        Output = Output + "You cheated!  You didn't specify a color!<P>"     
    if comment != None:
        Output = Output + "In addition, you said:<BR>" + comment + "<P>"     
 
    Display(Output) 
 
###
### 실제 스크립트 여기서 시작
### 
 
### CGI 요구 평가
form = cgi.FieldStorage() 
 
### "key" 는 폼에서 숨겨진 요소임.

try:
    key = form["key"].value
except:
    key = None 
if key == "process":
    ProcessForm(form)
else:
    DisplayForm()