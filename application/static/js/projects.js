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

    $('#editModal').on('hidden.bs.modal', function() {
        $f = $(this);
        if ($f.find("input[name='id']").val()) {
            $f.find("form.modal-content")[0].reset();
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
                bootstrap.Modal.getOrCreateInstance('#editModal').hide();
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
                bootstrap.Modal.getOrCreateInstance($m).show();
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
    });

    $('.btn-edit, .btn-project-edit').click(function() {
        var pid = $(this).data('id');
        $.getJSON( "/api/project/load/"+pid+"/edit" )
            .done(function( json ) {
                var $m = $('#editModal');
                $m.find('#iId').val(json.id);
                $m.find('#iTitle').val(json.title);
                $m.find('#iDescription').val(json.description);
                $m.find('#iBudget').val(json.budget);
                $m.find('#iStart').parent().datepicker('update', json.start);
                $m.find('#iDeadline').parent().datepicker('update',json.deadline);
                $m.find('#iStatus').val(json.status);
                bootstrap.Modal.getOrCreateInstance('#viewModal').hide();
                bootstrap.Modal.getOrCreateInstance('#editModal').show();
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
    });

    $('.action-archive-project').click(function(event) {
        event.preventDefault();
        $card = $(this).closest('form');
        pid = $card.find("input[name='pid']").val()
        ptt = $card.find(".card-title").text()
        tfk_confirm('Do you want to archive the following project?<br /> <b>'+ptt+'</b>');
    });
    $('.action-delete-project').click(function(event) {
        event.preventDefault();
        $card = $(this).closest('form');
        pid = $card.find("input[name='pid']").val()
        ptt = $card.find(".card-title").text()
        var what = prompt("please enter 'DELETE' to confirm deletion of\n\n   '"+ptt+"'\n\nAttention:\n - All tasks will be deleted\n - Action is permanent.");
        if (what == 'DELETE') {
            alert('Deleting project #'+pid);
        } else {
            alert("Cancelled !")
        }
    });
});

