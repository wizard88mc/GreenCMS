// JavaScript Document

window.onload = function() {
	
	var xmlhttp;
	
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}
	else {
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	xmlhttp.onreadystatechange = function() {
		
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			
			document.getElementById("preloader").style.display = "none";
			
			var listExams = document.createElement("ul");
			listExams.innerHTML = xmlhttp.responseText;
			
			var paragraph = document.createElement("p");
			paragraph.innerHTML = "ATTENZIONE: Vengono visualizzati gli esami della Laurea e della Laurea Magistrale";
			
			document.getElementById("contentsLong").appendChild(paragraph);
			
			document.getElementById("contentsLong").appendChild(listExams);
			
		}
		else {
			document.getElementById("preloader").style.display = "block";
		}
		
	}
	
	xmlhttp.open("GET", "../../cgi-bin/RetrieveListExamsAjax.cgi", true);
	xmlhttp.send();
	
}
