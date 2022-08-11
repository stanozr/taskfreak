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

    $('.action-archive-project').click(function() {
        $card = $(this).closest('form').find('.card-header');
        pid = $card.find("input[name='pid']").val()
        ptt = $card.find("input[name='title']").val()
        tfk_confirm('Do you want to archive project <b>'+ptt+'</b> ?');
    });
    $('.action-delete-project').click(function() {
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

