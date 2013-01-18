#!/usr/bin/env python
#encoding: utf-8

'''
last updated: November 8, 2010
[update]

'''
import cgi
import cgitb; cgitb.enable()
import time 

from AnnoFix import *

def getType(asin):
	asin_type_dict = {
	'B0018OKX68':'levis',
	'B0018OMIMK':'levis',
	'B0018OR118':'levis',

	'B0018P397W':'women_levis',
	'B0018P6FVY':'women_levis',
	'B0018P3GK2':'women_levis',
	'B0018PC75W':'women_levis',
	'B0018P4YQW':'women_levis',

	'B000EXW1JQ':'over50',
	'B000EQ6BC6':'over50',
	'B000CMDNBE':'over50',
	'B0007XPV8G':'over50',
	'B002EQAMV0':'over50'
	}
	type = asin_type_dict[asin]
	return type 

def getPrdTitle(type,asin):
	f = open('../prd_classify/prd_name/asin_table.dat')
	data = f.read()
	asinDict = eval(data)
	if asinDict.has_key(asin):
		return asinDict[asin][0]
	else:
	 	return ''

def postParamsFromURI():
    params = cgi.FieldStorage()

    #id,text
#    type = params.getvalue("type", None)
    asin = params.getvalue("asin", None)
    view = params.getvalue("view", None)
    return asin, view


if __name__ == '__main__':
	print 'Content-Type: text/html\n'

	asin,view  = postParamsFromURI()

#	print '<html>'
	print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'

	print '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ko" lang="ko">'

	print '<head><style>div{font-family:"Arial";}'
	print 'h2{font-family:"Arial"; font-size:"20pt"; color:"rgb(0,0,255)";}'
	print 'h3{font-family:"Arial"; font-size:"12pt";}'
	print '</style>'

	print '<script type="text/javascript" src="httpRequest.js"></script>'
	print '''<script type="text/javascript">
	
	function func5(anno_type, chkid, type,review_num,st_num, cbid1,cbid2, ip){
		
		//var len = w_list_len;
		var w_span = "";
		var len = document.f.elements[chkid].length;
		for(i=0; i<len; i++)
		{
			if(document.f.elements[chkid][i].checked == true)
			{ 
				w_span += i+'#';
			}
		}

		var target_type = document.f.elements[cbid1].value
		var confidence = document.f.elements[cbid2].value

		arg1 = type
		arg2 = review_num
		arg3 = st_num
		arg4 = w_span 
		arg5 = target_type
		arg6 = anno_type
		arg7 = confidence 
		arg8 = ip

		accID1 = cbid1;
		accID2 = cbid2;
		var params = ("arg1="+encodeURIComponent(arg1)+"&arg2="+encodeURIComponent(arg2)+"&arg3="+encodeURIComponent(arg3)+"&arg4="+encodeURIComponent(arg4)+"&arg5="+encodeURIComponent(arg5)+"&arg6="+encodeURIComponent(arg6)+"&arg7="+encodeURIComponent(arg7)+"&arg8="+encodeURIComponent(arg8));
		
		sendRequest("ajaxproc_fix.py", params, callback, "GET");
	}
	function func_coref(anno_type, asin, ment_str,ment_i, ment_num, ment_type,ant_str,ant_i, ant_num, ant_type,cbid1,ip){
		
		var coref_type = document.f.elements[cbid1].value

		arg1 = anno_type
		arg2 = asin 
		arg3 = ment_str
		arg4 = ment_i
		arg5 = ment_num
		arg6 = ment_type
		arg7 = ant_str
		arg8 = ant_i
		arg9 = ant_num
		arg10 = ant_type
		arg11 = coref_type
		arg12 = ip

		accID1 = cbid1;

		var params = ("arg1="+encodeURIComponent(arg1)+"&arg2="+encodeURIComponent(arg2)+"&arg3="+encodeURIComponent(arg3)+"&arg4="+encodeURIComponent(arg4)+"&arg5="+encodeURIComponent(arg5)+"&arg6="+encodeURIComponent(arg6)+"&arg7="+encodeURIComponent(arg7)+"&arg8="+encodeURIComponent(arg8)+"&arg9="+encodeURIComponent(arg9)+"&arg10="+encodeURIComponent(arg10)+"&arg11="+encodeURIComponent(arg11)+"&arg12="+encodeURIComponent(arg12));
	
		sendRequest("ajaxproc_coref.py", params, callback, "GET");
	}


	function clear(chkid) {
		var len = document.f.elements[chkid].length;
		for(i=0; i<len; i++)
		{
			if(document.f.elements[chkid][i].checked == true)
			{
				document.f.elements[chkid][i].checked = false
			}
		}
	}
	function callback() {
		if (oReq.readyState == 4 ||  oReq.readyState=="complete") {	//readyState is 4 if loaded
			if (oReq .status == 200) {	
				alert(oReq.responseText);
				result = oReq.responseText.split('\t');
				if(result[0] != "coref") {
					chkid = 'chk'+result[2]+'#'+result[3];
					clear(chkid);
					document.f.elements[accID1].style.backgroundColor = '#FF0099';
					document.f.elements[accID2].style.backgroundColor = '#FF0099';
				}
				else {
					document.f.elements[accID1].style.backgroundColor = '#FF0099';
				}
			}
		}
		else
		{
			//alert("error : "+oReq.readyState+"/"+oReq.responseText); 
		}
	}
	</script>



	'''
	print '</head>'
	print '<body>'
	print '<form name="f">'
	print '<div>[Product Referring Term Annotation] <br></div>'
	print "<div><b><font color='blue'>Blue</font></b>: current product <br></div>"
	print "<div><b><font color='red'>Red</font></b>: previous product (purchased in the past) <br></div>"
	print "<div><b><font color='green'>Green</font></b>: non-temporal entity <br></div>"
	print "<div><b><font color='orange'>Orange</font></b>: current + previous <br></div>"

	print '<p>'
	type = getType(asin)
	prdTitle = getPrdTitle(type,asin)
	print "<div>Product: %s, %s, %s<br></div>" % (type,asin,prdTitle)
	AnnoFixReview(type,asin,view)

#	print unicode(result_text,'cp949').encode('utf-8')
	print '</form>'
	print '</body>'
	print '</html>'
	
