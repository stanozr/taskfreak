$('document').ready(function() {

    $( "#preferences-form" ).submit(function( event ) {
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
            }
        });
        event.preventDefault();
    });

});