$('document').ready(function() {
    var drake = dragula({
        isContainer: function (el) {
            return el.classList.contains('kanban-tasks');
        },
        revertOnSpill: true
    });

    $('.task-title').click(function() {
        $t = $(this);
        $('#viewModal .modal-header').find('h5').text($t.text());
        new bootstrap.Modal('#viewModal').show();
    });

});