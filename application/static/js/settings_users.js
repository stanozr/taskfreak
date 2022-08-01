$('document').ready(function() {
    $f = $('#editModal');
    let frkEditModal = new bootstrap.Modal($f);
    $f.on('hidden.bs.modal', function() {
        $f.find("input[name='email']").removeClass('form-control-plaintext').addClass('form-control').prop('readonly', false);
        $f.find(".modal-content")[0].reset();
    });
    $(".row-user .btn-edit").click(function() {
        $r = $(this).closest('.row-user');
        uid = $r.data('id');
        $.getJSON( "/api/users/load/"+uid )
            .done(function( json ) {
                $f.find("input[name='id']").val(json.id);
                $f.find("input[name='name']").val(json.name);
                $f.find("input[name='email']").val(json.email).removeClass('form-control').addClass('form-control-plaintext').prop('readonly', true);
                $f.find("select[name='roles']").val(json.roles);
                frkEditModal.show();
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
    });
    $( "#user-form" ).submit(function( event ) {
        $t = $(this);
        $.ajax({
            method: "POST",
            url: $t.attr('action'),
            data: $t.serialize()
        }).done(function (data) {
            if (data.error) {
                toasted(data.error, 'text-bg-danger');
            } else {
                frkEditModal.hide();
                location.reload();
            }
        });
        event.preventDefault();
    });
});