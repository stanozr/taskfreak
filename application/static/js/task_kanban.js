$('document').ready(function() {
    var drake = dragula({
        isContainer: function (el) {
            return el.classList.contains('kanban-tasks');
        },
        revertOnSpill: true
    });
});