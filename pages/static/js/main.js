var hamFirst = $("#first");
var hamSecond = $("#second");
var hamThird = $("#third");

function hamToggle(e){
    var menu = $("#menu");
    console.log(menu.css("width"));
    if(menu.css("width") == "0px"){
        menu.css("width","90%");
    }   else{
        menu.css("width","0%");
    }
    hamFirst.toggleClass("firstChange");
    hamSecond.toggleClass("secondChange");
    hamThird.toggleClass("thirdChange");
    console.log(document.getElementById("menu"));
}


$(document).ready(function () {
    $('#lizenzTabelle').DataTable();
    $('.dataTables_length').addClass('bs-select');
    });
