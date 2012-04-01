// JavaScript Document

window.onload = function() {
	
	var toHide = document.getElementsByTagName("dd");
	
	for (i = 0; i < toHide.length; i++) {
		if (toHide.item(i).className =="hide") {
			toHide.item(i).style.display = "none";
		}
	}
	
	var xmlhttp;
	//recupero le ultime news che riguardano la laurea
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}
	else {
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	
	xmlhttp.onreadystatechange = function() {
		
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			
			//prendo la radice con le news
			var activeNews = xmlhttp.responseXML.documentElement.getElementsByTagName("ActiveNews");
			
			var dlNews = document.getElementById("dlNews");
			
			//conto quante news inserisco
			var count = 0;
		
			for (i = 0; i < activeNews.length && i < 3; i++) {  //stampo al massimo 3 news
				
				//prendo id news
				var id = activeNews[i].getElementsByTagName("ID")[0].firstChild.nodeValue;
				//prendo data news
				var date = activeNews[i].getElementsByTagName("Date")[0].firstChild.nodeValue;
				var dateNews = new Date();
				dateNews.setFullYear(date.substring(0, 4),date.substring(5, 7) - 1,date.substring(8, 10));
				var today = new Date();
				if (today > dateNews) {
				    count = count + 1;
				//prendo data e la correggo per metterla nel formato gg/mm/aaaa
				var dateCorrect = date.substring(8, 10) + "/" + date.substring(5, 7) + "/" + date.substring(0, 4);
				//prendo titolo news
				var title = activeNews[i].getElementsByTagName("Title")[0].firstChild.nodeValue;
				
				//prendo testo news e ne recupero i primi 100 caratteri
				var text = activeNews[i].getElementsByTagName("Text")[0].firstChild.nodeValue;
				text = text.replace("[link]", "").replace("[/link]", "");
				text = text.substr(0, 100) + ". . .";
				
				//inserisco un elemento html <dt>, con all'interno un link alla news
				//testo del link titolo della news
				var dtElementTitle = document.createElement("dt");
				
				var anchorTarget = "/cgi-bin/ReadNews.cgi?newsID=" + id;
				var anchorNews = document.createElement("a");
				anchorNews.href = anchorTarget;
				anchorNews.innerHTML = title;
				
				dtElementTitle.appendChild(anchorNews);
				
				//inserisco all'interno di un dd la data della news
				var ddElementDate = document.createElement("dd");
				ddElementDate.setAttribute("class", "newsDate");
				ddElementDate.innerHTML = dateCorrect;
				
				//inserisco all'interno di un dd il testo iniziale della news
				var ddElementText = document.createElement("dd");
				ddElementText.setAttribute("class", "newsContent");
				ddElementText.innerHTML = text;
				
				//inserisco tutto nel dl della pagina dedicato alle news
				dlNews.appendChild(dtElementTitle);
				dlNews.appendChild(ddElementDate);
				dlNews.appendChild(ddElementText);
				}
			}
			
			//nel caso in cui non ci siano news, stampo messaggio che indica l'assenza
			if (count == 0) {
				var ddNoNews = document.createElement("dd");
				ddNoNews.innerHTML = "Attualmente non sono presenti news";
				dlNews.appendChild(ddNoNews);
			}
			
			//inserisco un link all'archivio che stampa le news
			var ddArchive = document.createElement("dd");
			var anchorArchive = document.createElement("a");
			var anchorTarget = "/cgi-bin/News.cgi";
			anchorArchive.href= anchorTarget;
			anchorArchive.innerHTML = "Archivio";
			ddArchive.appendChild(anchorArchive);
			
			dlNews.appendChild(ddArchive);
		
		}
		
		
	}
	
	xmlhttp.open("GET", "xml_files/ActiveNews.xml", true);
	xmlhttp.send();
	
	
	
	//inizia parte di script per recuperare i prossimi due seminari inseriti
	if (window.XMLHttpRequest) {
		xmlhttpSecond = new XMLHttpRequest();
	}
	else {
		xmlhttpSecond = new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	
	xmlhttpSecond.onreadystatechange = function() {
		
		if (xmlhttpSecond.readyState == 4 && xmlhttpSecond.status == 200) {
			
			//prendo la radice con gli eventi programmati
			eventsList = xmlhttpSecond.responseXML.documentElement.getElementsByTagName("Event");
			
			var dlEvents = document.getElementById("dlEvents");
			
			var count = 0;
		
			for (i = 0; i < eventsList.length && i < 2; i++) {  //stampo al massimo due eventi
				
				//recupero data attuale
				var today = new Date();
				
				//recuperto data dell'evento
				var eventDateXML = eventsList[i].getElementsByTagName("Date")[0].firstChild.nodeValue;
				var year = parseInt(eventDateXML.substring(0, 4));
				var month = parseInt(eventDateXML.substring(5, 7)) - 1;
				var day = parseInt(eventDateXML.substring(8, 10)) + 1;
				var eventDate = new Date(year, month, day);
				
				//se la data dell'evento è maggiore rispetto a quella attuale significa che l'evento è da visualizzare
				if (eventDate > today) {
				
					count = count + 1;
					
					//recupero id
					var id = eventsList[i].getElementsByTagName("ID")[0].firstChild.nodeValue;
					//recupero ora
					var time = eventsList[i].getElementsByTagName("Time")[0].firstChild.nodeValue;
					//recupero titolo evento
					var title = eventsList[i].getElementsByTagName("Title")[0].firstChild.nodeValue;
					//recupero luogo
					var place = eventsList[i].getElementsByTagName("Place")[0].firstChild.nodeValue;
					//recupero speaker
					var speaker = eventsList[i].getElementsByTagName("Speaker")[0].firstChild.nodeValue;
					
					var dateCorrect = eventDateXML.substring(8, 10) + "/" + eventDateXML.substring(5, 7) + "/" + eventDateXML.substring(0, 4);
					var timeCorrect = time.substring(0, 5);
					
					//inserisco il titolo dentro un dt, con un link per andare alla descrizione del seminario
					var dtElementTitle = document.createElement("dt");
					
					var anchorTarget = "/cgi-bin/Seminari.cgi#" + id;
					var anchorNews = document.createElement("a");
					anchorNews.href = anchorTarget;
					anchorNews.innerHTML = title;
					
					dtElementTitle.appendChild(anchorNews);
					
					//inserisco all'interno di un dd la data del seminario, l'ora ed il luogo
					var ddElementDate = document.createElement("dd");
					ddElementDate.setAttribute("class", "newsDate");
					ddElementDate.innerHTML = dateCorrect + " " + timeCorrect + ", " + place;
					
					//inserisco speaker in un dd
					var ddElementSpeaker = document.createElement("dd");
					ddElementSpeaker.setAttribute("class", "newsContent");
					ddElementSpeaker.innerHTML = "Speaker: " + speaker;
					
					//appendo il tutto ad dl di id dlEvents
					dlEvents.appendChild(dtElementTitle);
					dlEvents.appendChild(ddElementDate);
					dlEvents.appendChild(ddElementSpeaker);
				}
			}
			
			//nel caso in cui non ci siano seminari stampo messaggio
			if (count == 0) {
				var ddNoEvent = document.createElement("dd");
				ddNoEvent.innerHTML = "Non ci sono eventi in programma";
				dlEvents.appendChild(ddNoEvent);
			}
			
			//inserisco link all'archivio
			var ddArchive = document.createElement("dd");
			var anchorArchive = document.createElement("a");
			var anchorTarget = "/cgi-bin/Seminari.cgi";
			anchorArchive.href= anchorTarget;
			anchorArchive.innerHTML = "Archivio";
			ddArchive.appendChild(anchorArchive);
			
			dlEvents.appendChild(ddArchive);
		
		}
		
		
	}
	
	xmlhttpSecond.open("GET", "xml_files/EventMailingListContact.xml", true);
	xmlhttpSecond.send();
}