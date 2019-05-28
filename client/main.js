

function buttonClick() {
    searchDatabase();
    return false;
}
function searchDatabase() {
    document.getElementById("test").innerHTML = "You entered: " + document.getElementById("term").value;
}

function sendAjaxRequest(element,urlToSend) {

}


$(document).ready(function(){
    $("#searchButton").click(function(){
        $.ajax({url: "https://cat-fact.herokuapp.com/facts", success: function(result){
        $("#facts").html(result);
        }});
    });
});

/*  search up how to add ajax call to button  */