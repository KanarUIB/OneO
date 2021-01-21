
$(document).ready(function () {
  $('#lizenzTabelle').DataTable({
   "scrollY":"70vh",
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
   "scrollY":"70vh",

         "info":     false


  });

  $('#kundenListe').DataTable({

         "paging":   false,
        "ordering": false,
        "info":     false

  });












});
