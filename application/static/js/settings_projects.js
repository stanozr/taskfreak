$('document').ready(function() {
    var drake = dragula({
        isContainer: function (el) {
            return el.classList.contains('project-lists');
        },
        moves: function (el, container, handle) {
            return handle.classList.contains('gu-handle');
        },
        revertOnSpill: true
    });
    $('.action-archive-project').click(function() {
        $card = $(this).closest('form').find('.card-header');
        console.log($card);
        pid = $card.find("input[name='pid']").val()
        ptt = $card.find("input[name='title']").val()
        if (confirm("Click OK to archive the following project:\n-> "+ptt)) {
            alert('Archiving project #'+pid);
        } else {
            alert("Cancelled !")
        }
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

