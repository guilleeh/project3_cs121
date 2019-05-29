function buttonClick() {
    event.preventDefault()
    searchDatabase();
    return false;
}
function searchDatabase() {
    // document.getElementById("test").innerHTML = "You entered: " + document.getElementById("term").value;
    let searchQuery = document.getElementById("term").value;
    displayResults(searchQuery);
}

function template(data) {
    var html = '<ul>';
    $.each(data, function(index, item){
        html += '<li>'+ item +'</li>';
    });
    html += '</ul>';
    return html;
}

function displayResults(query) {
    console.log("HERE")
    $('#pagination-container').pagination({
        dataSource: [1,2,3,4,5,6,7,8,98,7,6,5,4,3,2,2,3,4,5,6,7,8,98,7,6,5,4,3,2,2,3,4,5,6,7,8,98,7,6,5,4,3,2,2,3,4,5,6,7,8,98,7,6,5,4,3,2,2,3,4,5,6,7,8,98,7,6,5,4,3,2,2,3,4,5,6,7,8,98,7,6,5,4,3,2,2,3,4,5,6,7,8,98,7,6,5,4,3,2,2,3,4,5,6,7,8,98,7,6,5,4,3,2],
        callback: function(data, pagination) {
            // template method of yourself
            var html = template(data);
            $('#data-container').html(html);
        }
    })
    // var request = new XMLHttpRequest();
    // request.open('GET', 'http://localhost:5000/search?search=' + query, true);

    // request.onload = function() {
    //     if (request.status >= 200 && request.status < 400) {
    //         var data = JSON.parse(request.responseText);
    //         // $('#pagination-container').pagination({
    //         //     dataSource: data[0],
    //         //     callback: function(data, pagination) {
    //         //         // template method of yourself
    //         //         var html = template(data);
    //         //         $('#data-container').html(html);
    //         //     }
    //         // })
    //         data = data[0];
            // let content = document.getElementById('json-response')
            // for(let i = 0; i < data.length; i++) {
            //     var para = document.createElement("P");
            //     var t = document.createTextNode("File: " + data[i].file + ", Score: " + data[i].tfidf + ", URL: " + data[i].url + ", Frequency: " + data[i].frequency + '\n');
            //     para.appendChild(t);
            //     content.appendChild(para);
            // }
        // } else {

        // }
    // }

    // request.onerror = function (e) {
    //     console.alert(e)
    // }

    // request.send();
    // let json_data = {
    //     "Document1": "text",
    //     "Document2": "text2",
    //     "Document3": "text3",
    //     "Document4": "text4",
    //     "Document5": "text5",
    //     "Document6": "text6",
    //     "Document7": "text7",
    //     "Document8": "text8",
    //     "Document9": "text9",
    //     "Document0": "text10",
    //   }
    //   var list = document.getElementById('json-response');
    //   for (var key in json_data) {

    //     var entry = document.createElement('li');


    //     //entry.appendChild(document.createTextNode(key));
    //     // var link = document.createElement('a');
    //     // link.href = "#";
    //     // link.innerText = "click";
    //     // entry.appendChild(link);

    //     entry.insertAdjacentHTML("beforeend",'<a href="#">'+key+'</a>' + " Description");

    //     list.appendChild(entry);
    //   }
      
}

/*  search up how to add ajax call to button  */