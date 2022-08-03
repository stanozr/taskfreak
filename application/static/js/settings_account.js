$('document').ready(function() {

    $( "#account-form" ).submit(function( event ) {
        $t = $(this);
        $.ajax({
            method: "POST",
            url: $t.attr('action'),
            data: $t.serialize()
        }).done(function (data) {
            if (data.error) {
                tfk_toasted(data.error, 'text-bg-danger');
            } else {
                tfk_toasted(data.success, 'text-bg-success');
                $('#user-avatar, .btn-nav.btn-user').html(data.avatar);
            }
        });
        event.preventDefault();
    });

})