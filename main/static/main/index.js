document.addEventListener('DOMContentLoaded', function () {
    let quote_id = 0;
    let text = document.getElementById('quote');
    let errorSound = document.getElementById('errorSound');
    let finished = false;
    let i = 0;
    let charList = [];
    for(i ; i< text.innerHTML.trim().length ; i++){
        charList[i] = text.innerHTML.trim().charAt(i);
    }
    let timer = null;
    let hoverText = "";
    // console.log(charList);
    let inputList = [];
    $("#quoteInput").bind('keypress keydown', function (event) {
        let eventType = event.type;
        // console.log(eventType);
        if (eventType == 'keypress' && !finished) {
            if (event.keyCode && event.keyCode != 13 && event.keyCode != 27 && event.keyCode !=8) {
                // console.log(String.fromCharCode(event.charCode));
                // console.log(event.keyCode);

                inputList.push(String.fromCharCode(event.charCode));
                if (check(charList, inputList)) {
                    
                    let quote = document.getElementById('quote');
                    if(inputList.length == 1){ // score and time start from here 
                        quote.innerHTML = quote.innerHTML.replace(String.fromCharCode(event.charCode), `<span style='background-color: yellow; font-weight: bold; color: green'>${String.fromCharCode(event.charCode)}</span>`);
                        hoverText = convertArrayToText(inputList);
                        timer = setInterval(setTime, 10); 
                        
                    }
                    else{
                        quote.innerHTML = quote.innerHTML.replace(`</span>${String.fromCharCode(event.charCode)}`, `${String.fromCharCode(event.charCode)}</span>`);
                        if (charList.length === inputList.length) {  //finished writing the text
                            finished = true;
                            clearInterval(timer);
                            let totalMinutes = (seconds/100) /60;
                            let totalWords = getNumberOfWords(charList);
                            let win = document.getElementById('winSound');
                            let temp = document.getElementById('your_score');
                            temp.innerHTML =(totalWords/totalMinutes).toFixed(2);
                            temp.parentElement.style.backgroundColor = "lightgreen";
                            temp.parentElement.style.color = "white";
                            win.play();

                            //updating the database
                            fetch('/new_record',{
                                method : 'POST',
                                body : JSON.stringify({
                                    'quote_id' : quote_id,
                                    best_time : totalWords/totalMinutes
                                })
                                
                            });
                            

                            document.getElementById('quoteInput').value = "";

                        }

                    }

                   
                }
                else {
                    errorSound.play();
                }

                // console.log("textList = " + charList);
                // console.log("inputList = " + inputList);
            }
        }
        else {
            if (event.keyCode == 8) {

                hoverText = convertArrayToText(inputList);
                let quote = document.getElementById('quote');
                quote.innerHTML = quote.innerHTML.replace(`${hoverText.charAt(hoverText.length - 1)}</span>`, `</span>${hoverText.charAt(hoverText.length - 1)}`);
                hoverText = hoverText.slice(0, -1);
                inputList.pop();
            }
            else if(event.keyCode == 27){

            }
            else if (event.keyCode == 13){ //enter pressed
                document.getElementById('first-text').style.display= "none";
                clearInterval(timer);
                seconds = 0;
                fetch('/rand_quote')
                    .then(response => response.json())
                    .then(result => {
                        document.getElementById('quote').innerHTML = result.quote;
                        document.getElementById('quoteAuther').innerHTML = result.auther;
                        document.getElementById('quoteTitle').innerHTML = result.title;
                        document.getElementById('quotePublisher').innerHTML = result.username;
                        document.getElementById('best_username').innerHTML = result.best_username;
                        document.getElementById('best_user_time').innerHTML = result.best_user_time;
                        document.getElementById('your_best_time').innerHTML = result.your_best_time;
                        document.getElementById('world_rank').innerHTML = result.your_world_rank;
                        document.getElementById('country_rank').innerHTML = result.your_country_rank;
                        document.getElementById('like-count').innerHTML = result.likes;
                        document.getElementById('dislike-count').innerHTML = result.dislikes;


                        charList = convertTextToArray(document.getElementById('quote').innerHTML);
                        document.getElementById('user-records-graph').src = result.user_graph + "?t=" + new Date().getTime();
                        inputList = [];
                        best_time = result.best_time;
                        quote_id = result.id;
                        finished = false;


                        //generate countries table
                        let tableTag = document.getElementById('country-table');
                        //e.firstElementChild can be used.
                        let child = tableTag.lastElementChild;
                        while (child) {
                            tableTag.removeChild(child);
                            child = tableTag.lastElementChild;
                        }
                        let = placeCounter = 0;
                        for (const [key, value] of Object.entries(result.top_countries)){
                            placeCounter++;

                            let row = tableTag.appendChild(document.createElement('tr'));
                            if(placeCounter == 1){
                                row.appendChild(document.createElement('td')).innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="gold" class="bi bi-trophy-fill" viewBox = "0 0 16 16" > <path d="M2.5.5A.5.5 0 0 1 3 0h10a.5.5 0 0 1 .5.5c0 .538-.012 1.05-.034 1.536a3 3 0 1 1-1.133 5.89c-.79 1.865-1.878 2.777-2.833 3.011v2.173l1.425.356c.194.048.377.135.537.255L13.3 15.1a.5.5 0 0 1-.3.9H3a.5.5 0 0 1-.3-.9l1.838-1.379c.16-.12.343-.207.537-.255L6.5 13.11v-2.173c-.955-.234-2.043-1.146-2.833-3.012a3 3 0 1 1-1.132-5.89A33.076 33.076 0 0 1 2.5.5zm.099 2.54a2 2 0 0 0 .72 3.935c-.333-1.05-.588-2.346-.72-3.935zm10.083 3.935a2 2 0 0 0 .72-3.935c-.133 1.59-.388 2.885-.72 3.935z" /></svg >';
                            }
                            else if(placeCounter == 2){
                                row.appendChild(document.createElement('td')).innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="silver" class="bi bi-trophy-fill" viewBox = "0 0 16 16" > <path d="M2.5.5A.5.5 0 0 1 3 0h10a.5.5 0 0 1 .5.5c0 .538-.012 1.05-.034 1.536a3 3 0 1 1-1.133 5.89c-.79 1.865-1.878 2.777-2.833 3.011v2.173l1.425.356c.194.048.377.135.537.255L13.3 15.1a.5.5 0 0 1-.3.9H3a.5.5 0 0 1-.3-.9l1.838-1.379c.16-.12.343-.207.537-.255L6.5 13.11v-2.173c-.955-.234-2.043-1.146-2.833-3.012a3 3 0 1 1-1.132-5.89A33.076 33.076 0 0 1 2.5.5zm.099 2.54a2 2 0 0 0 .72 3.935c-.333-1.05-.588-2.346-.72-3.935zm10.083 3.935a2 2 0 0 0 .72-3.935c-.133 1.59-.388 2.885-.72 3.935z" /></svg >';

                            }
                            else if(placeCounter == 3){
                                row.appendChild(document.createElement('td')).innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#cd7f32" class="bi bi-trophy-fill" viewBox = "0 0 16 16" > <path d="M2.5.5A.5.5 0 0 1 3 0h10a.5.5 0 0 1 .5.5c0 .538-.012 1.05-.034 1.536a3 3 0 1 1-1.133 5.89c-.79 1.865-1.878 2.777-2.833 3.011v2.173l1.425.356c.194.048.377.135.537.255L13.3 15.1a.5.5 0 0 1-.3.9H3a.5.5 0 0 1-.3-.9l1.838-1.379c.16-.12.343-.207.537-.255L6.5 13.11v-2.173c-.955-.234-2.043-1.146-2.833-3.012a3 3 0 1 1-1.132-5.89A33.076 33.076 0 0 1 2.5.5zm.099 2.54a2 2 0 0 0 .72 3.935c-.333-1.05-.588-2.346-.72-3.935zm10.083 3.935a2 2 0 0 0 .72-3.935c-.133 1.59-.388 2.885-.72 3.935z" /></svg >';

                            }
                            else{
                                row.appendChild(document.createElement('td')).innerHTML  = placeCounter;
                            }
                            row.appendChild(document.createElement('td')).innerHTML = key;
                            row.appendChild(document.createElement('td')).innerHTML = value;
                            
                            
                        }



                        //handling likes and dislikes
                        document.getElementById('like-quote').replaceWith(document.getElementById('like-quote').cloneNode(true));
                        $('#like-quote').bind('click', () => {
                            console.log(result.id);

                            fetch('/like', {
                                method: 'PUT',
                                body: JSON.stringify({
                                    'quote_id': result.id,
                                })

                            })
                            .then(response =>{
                                if(response.status == 201){
                                    return response.json();
                                }
                            })
                            .then(result =>{
                                document.getElementById('like-count').innerHTML= result.like;
                                document.getElementById('dislike-count').innerHTML = result.dislike;
                            });
                        });

                        document.getElementById('dislike-quote').replaceWith(document.getElementById('dislike-quote').cloneNode(true));
                        $('#dislike-quote').bind('click', () => {
                            fetch('/dislike', {
                                method: 'PUT',
                                body: JSON.stringify({
                                    'quote_id': result.id,
                                })

                            })
                                .then(response => {
                                    if (response.status == 201) {
                                        return response.json();
                                    }
                                })
                                .then(result => {
                                    document.getElementById('like-count').innerHTML = result.like;
                                    document.getElementById('dislike-count').innerHTML = result.dislike;
                                });
                        });

                        
                        
                        

                    });

                
            }
        }

    
        
    });

    
    
});




var seconds = 0;

function setTime() {
    ++seconds;
    // console.log(seconds);
}

function getNumberOfWords(charList){
    let i =0;
    let wordCount = 0;
    for (i; i < charList.length ; i++){
        if(charList[i] == " "){
            wordCount++;
        }
    }
    wordCount++;
    return wordCount;
}

function convertTextToArray(text){
    let i = 0;
    let charList = [];
    for (i; i < text.trim().length; i++) {
        charList[i] = text.trim().charAt(i);
    }
    return charList;
}

function convertArrayToText(array){
    let i = 0;
    let text = "";
    for (i; i < array.length; i++) {
        text = text + array[i];
    }
    return text;
}

function check(textList, input){
    let i = 0;
    let result = true;
    for (i; i<input.length ; i++){
        if(input[i] != textList[i]){
            return false;
        }
        
    }
    return result;
}


function publishQuote(){
    let auther = document.getElementById('publish-quote-auther');
    let title = document.getElementById('publish-quote-title');
    let content = document.getElementById('publish-quote-content');
    let parent = auther.parentElement.parentElement;
    var toggle = true;
    
    

    if(auther.value.trim() != "" && title.value.trim() != "" && content.value.trim() != ""){

        fetch('/post_quote', {
            method: 'POST',
            body: JSON.stringify({
                auther: String(auther.value.trim()),
                title: String(title.value.trim()),
                content: String(content.value.trim()),
            })
        })
            .then(response =>{
                if(response.status == 201){
                    $('#writepopUp').modal('hide');
                    auther.value = "";
                    title.value = "";
                    content.value = "";
                }
            })

    }
    else if (parent.lastChild.nodeName == 'P'){
        
        
    }
    else{

        let errMess = document.createElement('p');
        errMess.style.color = "red";
        errMess.innerHTML = "*  ALL FIELDS ARE REQUIRED";
        parent.appendChild(errMess);
    }

}


function like(quote_id){

}