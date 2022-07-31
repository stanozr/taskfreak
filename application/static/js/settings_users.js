$('document').ready(function() {
    $f = $('#editModal');
    $f.on('hidden.bs.modal', function() {
        $f.find(".modal-content")[0].reset();
    });
    $(".row-user .btn").click(function() {
        $r = $(this).closest('.row-user');
        uid = $r.data('id');
        $.getJSON( "/api/users/load/"+uid )
            .done(function( json ) {
                $f.find("input[name='name']").val(json.name);
                $f.find("input[name='email']").val(json.email);
                $f.find("select[name='roles']").val(json.roles);
                new bootstrap.Modal($f).show();
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
    });
});