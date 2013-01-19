<Script Type="text/javascript">
    function getSpan(num) {
		var checked = document.getElementsByName('check'+num);

		var nCheck = 0;
		for(var i = 0;i<checked.length;i++) {
			if(checked[i].checked == true)
				nCheck++;
		}
		
		if(nCheck == 1) {
			if(!confirm('use one size span?'))
				return [-1,-1];
				
			for(var i = 0;i<checked.length;i++) {
				if(checked[i].checked == true) {
					 for(var j = 0;j<checked.length;j++)
            			checked[j].checked = false;
					return [i, i];
				}
			}
		}
		else if(nCheck != 2) {
			alert('check start and end');
			return [-1,-1];
		}
		else {
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

			return [from, to];
		}
    }
    
    function addNewClause(num) {
		var spanRtn = getSpan(num);
		if(spanRtn[0] == -1)
			return;

       	from = spanRtn[0];
       	to = spanRtn[1];
		
		var clauseInfoDiv = document.getElementsByName('clauseInfoDiv'+num)[0];
		var newClauseInfos = document.createElement('div');
		newClauseInfos.setAttribute('name', 'clauseInfos'+num);
		newClauseInfos.style.border = '1px solid';
		newClauseInfos.id = 'clauseInfos'+uniqueId;
		innerHTML = "<input type='hidden' name='clauseValue"+num+"' value='"+1+"'/>"+
                   "<input type='button' value='Add Clause' onclick='addClause("+num+","+uniqueId+")'/>"+
                   "<br/>";
        uniqueId++;
        
        var clauseType = document.getElementsByName('select'+num)[0];
        var tds = document.getElementsByName('td'+num);
        
        clauseStr = "";
		for(var j = Number(from);j<Number(to)+1;j++)
            clauseStr  += tds[j].innerText + ' ';
        clauseStr  += ' (' + clauseType.options[clauseType.selectedIndex].innerText + ', '+ document.getElementsByName('adinfo'+num)[0].value+')';
		//alert(clauseStr);
		
		var adinfo = document.getElementsByName('adinfo'+num)[0].value;
		var comment = document.getElementsByName('comment'+num)[0].value;
		if(adinfo == '')
			adinfo = ' '
		if(comment == '')
			comment = ' '
			
		innerHTML += "<div id='clauseInfo"+uniqueId+"'>"+
                        "<input type='text' size='"+clauseStr.length*2+"' onmouseout='highlightBack("+num+","+from+","+to+")' onmouseover='highlight("+num+","+from+","+to+")' value='"+clauseStr+"'/>"+
                        "<input type='hidden' name='clauseValue"+num+"' value='"+from+"'/>"+
                        "<input type='hidden' name='clauseValue"+num+"' value='"+to+"'/>"+
                        "<input type='hidden' name='clauseValue"+num+"' value='"+clauseType.options[clauseType.selectedIndex].value+"'/>"+
                        "<input type='hidden' name='clauseValue"+num+"' value='"+adinfo+"'/>"+
                        "<input type='hidden' name='clauseValue"+num+"' value='"+comment+"'/>"+
                        "<input type='button' value='Delete Clause' onclick='deleteClause("+num+", "+uniqueId+")'/>"+
                        "</div>";
		
		newClauseInfos.innerHTML = innerHTML;
		clauseInfoDiv.appendChild(newClauseInfos);
		clauseInfoDiv.appendChild(document.createElement('br'));
		uniqueId++;
		
		clauseInfoDiv.childNodes[0].value = Number(clauseInfoDiv.childNodes[0].value)+1;
    }
    
	function addClause(num, num2) { 
		var spanRtn = getSpan(num);
		if(spanRtn[0] == -1)
			return;

       	from = spanRtn[0];
       	to = spanRtn[1];
		
		var clauseInfos = document.getElementById('clauseInfos'+num2);
		var newClauseInfo = document.createElement('div');
		newClauseInfo.id = 'clauseInfo'+uniqueId;
       
        var clauseType = document.getElementsByName('select'+num)[0];
        var tds = document.getElementsByName('td'+num);
        
        clauseStr = "";
		for(var j = Number(from);j<Number(to)+1;j++)
            clauseStr  += tds[j].innerText + ' ';
        clauseStr  += ' (' + clauseType.options[clauseType.selectedIndex].innerText + ', '+ document.getElementsByName('adinfo'+num)[0].value+')';
		//alert(clauseStr);
		
		var adinfo = document.getElementsByName('adinfo'+num)[0].value;
		var comment = document.getElementsByName('comment'+num)[0].value;
		if(adinfo == '')
			adinfo = ' '
		if(comment == '')
			comment = ' '

		innerHTML = "<input type='text' size='"+clauseStr.length*2+"' onmouseout='highlightBack("+num+","+from+","+to+")' onmouseover='highlight("+num+","+from+","+to+")' value='"+clauseStr+"'/>"+
                        "<input type='hidden' name='clauseValue"+num+"' value='"+from+"'/>"+
                        "<input type='hidden' name='clauseValue"+num+"' value='"+to+"'/>"+
                        "<input type='hidden' name='clauseValue"+num+"' value='"+clauseType.options[clauseType.selectedIndex].value+"'/>"+
                        "<input type='hidden' name='clauseValue"+num+"' value='"+adinfo+"'/>"+
                        "<input type='hidden' name='clauseValue"+num+"' value='"+comment+"'/>"+
                        "<input type='button' value='Delete Clause' onclick='deleteClause("+num+", "+uniqueId+")'/>";
		
		newClauseInfo.innerHTML = innerHTML;
		clauseInfos.appendChild(newClauseInfo);
		uniqueId++;
		
		clauseInfos.childNodes[0].value = Number(clauseInfos.childNodes[0].value)+1; 
    }
    function deleteAllClauses(num) {
    	var clauseInfoDiv = document.getElementsByName('clauseInfoDiv'+num)[0];
    	var nChild = clauseInfoDiv.childNodes.length;
    	for(var i = 4;i<nChild;i++) 
    		clauseInfoDiv.removeChild(clauseInfoDiv.childNodes[4]);
    	clauseInfoDiv.childNodes[0].value = '0'; 
    }
    function deleteClause(num, num2) {
		var clauseInfo = document.getElementById('clauseInfo'+num2);
		var clauseInfos = clauseInfo.parentNode;
		clauseInfos.removeChild(clauseInfo);
		clauseInfos.childNodes[0].value = Number(clauseInfos.childNodes[0].value)-1;
		if(Number(clauseInfos.childNodes[0].value) == 0) {
			var clauseInfoDiv = clauseInfos.parentNode;
			var br = clauseInfos.nextSibling;
			clauseInfoDiv.removeChild(clauseInfos);
			clauseInfoDiv.removeChild(br);
			clauseInfoDiv.childNodes[0].value = Number(clauseInfoDiv.childNodes[0].value) - 1; 
		} 
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