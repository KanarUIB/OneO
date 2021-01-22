
$(document).ready(function () {
  $('#lizenzTabelle').DataTable({
   "scrollY":"50vh",

   language: {

    "emptyTable":     "Es sind keine Einträge vorhanden",
    "info":           "_START_ - _END_ von _TOTAL_ Einträgen",
    "infoEmpty":      "Showing 0 to 0 of 0 entries",
    "lengthMenu":     "_MENU_ Einträge anzeigen",
    "search":         "Schnellsuche:",
    "zeroRecords":    "No matching records found",
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

         "info":     false,
            language: {

    "emptyTable":     "Es sind keine Einträge vorhanden",
    "info":           "_START_ - _END_ von _TOTAL_ Einträgen",
    "infoEmpty":      "Showing 0 to 0 of 0 entries",
    "lengthMenu":     "_MENU_ Einträge anzeigen",
    "search":         "Schnellsuche:",
    "zeroRecords":    "No matching records found",
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

},

  });

});
