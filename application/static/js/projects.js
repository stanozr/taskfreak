$('document').ready(function() {
    var drake = dragula({
        isContainer: function (el) {
            return el.classList.contains('project-dragula');
        },
        moves: function (el, container, handle) {
            return handle.classList.contains('gu-handle');
        },
        revertOnSpill: true
    });

    $f = $('#editModal');
    let frkEditModal = new bootstrap.Modal($f);
    $f.on('hidden.bs.modal', function() {
        if ($f.find("input[name='id']").val()) {
            $f.find("form.modal-content").reset();
        }
    });
    
    $( "#project-form" ).submit(function( event ) {
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

    $('.btn-project-info').click(function(event) {
        event.preventDefault();
        var $m = $('#viewModal');
        var $f = $(this).closest('form');
        var pid = $f.find("input[name='id']").val();
        $.getJSON( "/api/project/load/"+pid+"/html" )
            .done(function( json ) {
                if ($f.hasClass('project-admin')) {
                    $m.find('.btn-edit').show();
                } else {
                    $m.find('.btn-edit').hide();
                }
                $m.find('.btn-edit').data('id', json.id);
                $m.find('.project-title').text(json.title);
                $m.find('.project-description').html(json.description);
                $m.find('.project-budget').text(json.budget);
                $m.find('.project-start').text(json.start);
                $m.find('.project-deadline').text(json.deadline);
                $m.find('.project-status').text(json.status);
                new bootstrap.Modal($m).show();
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
    });

    $('.action-archive-project').click(function(event) {
        event.preventDefault();
        $card = $(this).closest('form').find('.card-header');
        pid = $card.find("input[name='pid']").val()
        ptt = $card.find("input[name='title']").val()
        tfk_confirm('Do you want to archive project <b>'+ptt+'</b> ?');
    });
    $('.action-delete-project').click(function(event) {
        event.preventDefault();
        $card = $(this).closest('form').find('.card-header');
        console.log($card);
        pid = $card.find("input[name='pid']").val()
        ptt = $card.find("input[name='title']").val()
        var what = prompt("please enter 'DELETE' to confirm deletion of\n\n   '"+ptt+"'\n\nAttention:\n - All tasks will be deleted\n - Action is permanent.");
        if (what == 'DELETE') {
            alert('Deleting project #'+pid);
        } else {
            alert("Cancelled !")
        }
    });
});

