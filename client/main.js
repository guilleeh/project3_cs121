function buttonClick() {
    searchDatabase();
    return false;
}
function searchDatabase() {
    document.getElementById("test").innerHTML = "You entered: " + document.getElementById("term").value;
    let searchQuery = document.getElementById("term").value;
    displayResults(searchQuery);
}

function displayResults(query) {
    console.log("HERE")
    var request = new XMLHttpRequest();
    request.open('GET', 'http://localhost:5000/search?search=' + query, true);

    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            var data = JSON.parse(request.responseText);
            data = data[0];
            let content = document.getElementById('json-response')
            for(let i = 0; i < data.length; i++) {
                var para = document.createElement("P");
                var t = document.createTextNode("File: " + data[i].file + ", Score: " + data[i].tfidf + ", URL: " + data[i].url + ", Frequency: " + data[i].frequency + '\n');
                para.appendChild(t);
                content.appendChild(para);
            }
        } else {

        }
    }

    request.onerror = function (e) {
        console.alert(e)
    }


    request.send();
}

/*  search up how to add ajax call to button  */