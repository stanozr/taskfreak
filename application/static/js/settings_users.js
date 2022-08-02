$('document').ready(function() {
    $f = $('#editModal');
    // brtz = 'UTC'
    // try {
    //     brtz = Intl.DateTimeFormat().resolvedOptions().timeZone;
    // } catch(e){}
    // $f.find("select[name='timezone']").val(brtz);
    let frkEditModal = new bootstrap.Modal($f);
    $f.on('hidden.bs.modal', function() {
        $f.find("input[name='email']").removeClass('form-control-plaintext').addClass('form-control').prop('readonly', false);
        $f.find(".modal-content")[0].reset();
        // $f.find("select[name='timezone']").val(brtz);
    });
    $(".row-user .btn-edit").click(function() {
        $r = $(this).closest('.row-user');
        uid = $r.data('id');
        $.getJSON( "/api/users/load/"+uid )
            .done(function( json ) {
                $f.find("input[name='id']").val(json.id);
                $f.find("input[name='name']").val(json.name);
                $f.find("input[name='email']").val(json.email).removeClass('form-control').addClass('form-control-plaintext').prop('readonly', true);
                $f.find("select[name='timezone']").val(json.timezone);
                $f.find("select[name='roles']").val(json.roles);
                frkEditModal.show();
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
    });
    $(".row-user .btn-delete").click(function() {
        uname = $(this).closest('.row-user').find('.user-name').text();
        tfk_confirm('Please confirm removing user <b>'+uname+'</b><br /><span class="text-danger">This will disable the user, all data will remain.</span>', $(this).data('action'));
    });
    $( "#user-form" ).submit(function( event ) {
        $t = $(this);
        $.ajax({
            method: "POST",
            url: $t.attr('action'),
            data: $t.serialize()
        }).done(function (data) {
            if (data.error) {
                tfk_toasted(data.error, 'text-bg-danger');
            } else {
                frkEditModal.hide();
                location.reload();
            }
        });
        event.preventDefault();
    });
});