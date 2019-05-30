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

function template(data, pagination) {
    var html = '<ul>';
    console.log(pagination.pageNumber)
    var count = (pagination.pageNumber-1) * pagination.pageSize;
    if (pagination.pageNumber ===1) {
        count = 1
    }
    $.each(data, function(index, item){
        if (pagination.pageNumber ===1) {
            html += '<li>' + `${count} <a href="${item}" target="_blank">${item}</a>` +'</li>';
            count += 1;
            //gets current path instead of just url
        } else {
            count += 1
            html += '<li>' + `${count} <a href="${item}" target="_blank">${item}</a>` +'</li>';
        }
    });
    html += '</ul>';
    return html;
}

function displayResults(query) {
    console.log("HERE")
    var request = new XMLHttpRequest();
    request.open('GET', 'http://localhost:5000/search?search=' + query, true);

    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            var data = JSON.parse(request.responseText);
            data = data[0]
            for(var i = 0; i < data.length; i++) {
                data[i] = data[i].url;
                console.log(data[i])
            }
            $('#pagination-container').pagination({
                dataSource: data,
                autoHidePrevious: true,
                autoHideNext: true,
                callback: function(data, pagination) {
                    // template method of yourself
                    console.log(pagination)
                    var html = template(data, pagination);
                    $('#data-container').html(html);
                }
            })
            data = data[0];
        } else {

        }
    }

    request.onerror = function (e) {
        console.alert(e)
    }

    request.send();
      
}

/*  search up how to add ajax call to button  */