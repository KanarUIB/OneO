
$(document).ready(function () {
  $('#lizenzTabelle').DataTable({
   "scrollY":"50vh",

   language: {

    "emptyTable":     "Es sind keine Einträge vorhanden",
    "info":           "_START_ - _END_ von _TOTAL_ Einträgen",
    "infoEmpty":      "keine Einträge",
    "lengthMenu":     "_MENU_ Einträge anzeigen",
    "search":         "Schnellsuche:",
    "zeroRecords":    "Zu Ihrer Suche gibt es leider keine Einträge",
    "paginate": {

        "next":       ">",
        "previous":   "<"
    },
    "aria": {
        "sortAscending":  ": activate to sort column ascending",
        "sortDescending": ": activate to sort column descending"
    }
},
    initComplete: function () {
      this.api().columns().every( function () {
          var column = this;
          var search = $(`<input class="form-control form-control-sm" type="text" placeholder="suchen">`)
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

  $('#heartbeatTabelle').DataTable({
   "scrollY":"50vh",


            language: {

    "emptyTable":     "Es sind keine Einträge vorhanden",
    "info":           "_START_ - _END_ von _TOTAL_ Einträgen",
    "infoEmpty":      "keine Einträge",
    "lengthMenu":     "_MENU_ Einträge anzeigen",
    "infoFiltered":   "(von _MAX_ Einträgen)",
    "search":         "Schnellsuche:",
        "zeroRecords":    "Zu Ihrer Suche gibt es leider keine Einträge",
    "paginate": {

        "next":       ">",
        "previous":   "<"
    },
    "aria": {
        "sortAscending":  ": activate to sort column ascending",
        "sortDescending": ": activate to sort column descending"
    }
},




  });

  $('#kundenListe').DataTable({

         "paging":   false,
        "ordering": false,
        "info":     false,
           language: {

    "emptyTable":     "Es sind keine Einträge vorhanden",
    "search":         "Schnellsuche:",

}

  });

});

$("#gültig_bisSoftware").click(function(){
var gültigVon = $(this).prev().val();
$("#gültig_bisSoftware").attr("min",gültigVon);
});

$("#gültig_bisLizenz").click(function(){
var gültigVonLizenz = $(this).prev().val();
$("#gültig_bisLizenz").attr("min",gültigVonLizenz);
});

$(".trigger").click(function(){
    $(this).next(".toggle").slideToggle("slow");
  });

$(".anlegen.softwareBtn").click(function(){
    var standortID = Number($(this).prev().val());
    $("#standort_id_modal").val(standortID);
});

$(".cfgBtn").click(function(){
    var oldLicenseKey = $(this).prev().val();
    $("#alteLizenz").val(oldLicenseKey);
});


