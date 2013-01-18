<Script Type="text/javascript">
	numClause = 0;
    
    function getSpan(num) {
		var checked = document.getElementsByName('check'+num);

		var nCheck = 0;
		for(var i = 0;i<checked.length;i++) {
			if(checked[i].checked == true)
				nCheck++;
		}
		if(nCheck == 1) {
			if(!confirm('use one size span?'))
				return [-1,-1]
		}
		else if(nCheck != 2) {
			alert('check start and end');
			return;
		}

		var from, to;
		var isSecond = false;
		for(var i = 0;i<checked.length;i++) {
			if(checked[i].checked == true) {
				if(isSecond == false) {
					from = checked[i].value;
					isSecond = true;
				}
				else {
					to = checked[i].value;
					break;
				}
			}
		}
    }
    function addNewClause(num) {
		
    }
	function addClause(num) {
		var checked = document.getElementsByName('check'+num);
          
        var nCheck = 0;
        for(var i = 0;i<checked.length;i++) {
          if(checked[i].checked == true)
            nCheck++;
        }
        if(nCheck != 2) {
            alert('check start and end');
            return;
        }
              
        var from, to;
        var isSecond = false;
        for(var i = 0;i<checked.length;i++) {
            if(checked[i].checked == true) {
                if(isSecond == false) {
                    from = checked[i].value;
                    isSecond = true;
                }
                else {
                    to = checked[i].value;
                    break;
                }
            }
        }

        for(var i = 0;i<checked.length;i++)
            checked[i].checked = false;
                                  
        var newClause = document.createElement('div');

        var clauseType = document.getElementsByName('select'+num)[0];
        var tds = document.getElementsByName('td'+num);
        
        var clauseStr = "";

        for(var j = Number(from);j<Number(to)+1;j++)
            clauseStr  += tds[j].innerText + ' ';

        clauseStr  += ' (' + clauseType.options[clauseType.selectedIndex].innerText + ')';
          
        var str2 = from + ' ' + to +' '+clauseType.options[clauseType.selectedIndex].value;
        var clauseAdinfo = document.getElementsByName('adinfo'+num)[0];
        var clauseComment = document.getElementsByName('comment'+num)[0];
        str2 += '-' + clauseAdinfo.value + '-' + clauseComment.value;
        clauseAdinfo.value = '';
        clauseComment.value = '';

        if(document.getElementsByName('clause'+num)[0].value == '')
            document.getElementsByName('clause'+num)[0].value = str2;
        else
            document.getElementsByName('clause'+num)[0].value += '/' + str2;
              
        var clauseIdx = document.getElementsByName('div'+num)[0].length-3 
        newClause.innerHTML = "<input type=hidden name='clauseText"+num+"' value='"+str2+"'/>"
                              "<input type='text' size='250' onmouseout='highlightBack("+num+","+from+","+to+")' onmouseover='highlight("+num+","+from+","+to+")' name='clauseShow"+num+"' id='"+numClause+"'/>"
                              "<input type=button value='delete' onClick='deleteClause("+numClause+","+num+")'>";
                              
        newClause.childNodes[1].size = clauseStr.length*2;
        newClause.childNodes[1].value = clauseStr ;
        document.getElementsByName('div'+num)[0].appendChild(newClause);

        numClause++;
    }
      
    function deleteClause(num, num2) {
        var temp1 = document.getElementById(num).parentNode.parentNode;
        var temp2 = document.getElementById(num).parentNode;
        temp1.removeChild(temp2);
          
        var clauseTexts = document.getElementsByName('clauseText'+num2);
        var clauseStr = '';

        for(var i = 0;i<clauseTexts.length;i++) {
            clauseStr += clauseTexts[i].value;
            if(i <clauseTexts.length-1)
                clauseStr+='/';
        }

        document.getElementsByName('clause'+num2)[0].value = clauseStr
    }
    
    function highlight(num, from, to) {
        var tds = document.getElementsByName('td'+num);
        for(var i = from;i<=to;i++)
            tds[i].bgColor = 'yellow';
    }
      
    function highlightBack(num, from, to) {
        var tds = document.getElementsByName('td'+num);
        for(var i = from;i<=to;i++)
            tds[i].bgColor = 'white';
    }
</script>