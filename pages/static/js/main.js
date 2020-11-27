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

    $('#heartbeatsTabelle').DataTable({



    });
    $('.dataTables_length').addClass('bs-select');
    });



$(document).ready(function () {
  $('#lizenzTabelle').dataTable({

    initComplete: function () {
      this.api().columns().every( function () {
          var column = this;
          var search = $(`<input class="form-control form-control-sm" type="text" placeholder="Search">`)
              .appendTo( $(column.footer()).empty() )
              .on( 'change input', function () {
                  var val = $(this).val()

                  column
                      .search( val ? val : '', true, false )
                      .draw();
              } );

      } );
  }
  });
});
