$('document').ready(function(){

    var taskView = $('#viewModal');
    taskView.on('hidden.bs.modal', function() {
        $(this).find('.modal-header').removeClass('bg-danger bg-warning bg-info bg-light text-light');
        $(this).find('.task-priority').removeClass('border-danger border-warning border-info d-none');
    });
    $('.task-title').click(function() {
        $t = $(this);
        prcl = '';
        prcl2 = '';
        prtxt = '';
        prio = $t.closest('.task-row').find('.task-deadline');
        if (prio.hasClass('priority-3')) {
            prcl = 'bg-danger text-light';
            prcl2 = 'border-danger';
            prtxt = 'Urgent';
        } else if (prio.hasClass('priority-2')) {
            prcl = 'bg-warning';
            prcl2 = 'border-warning';
            prtxt = 'High priority';
        } else if (prio.hasClass('priority-1')) {
            prcl = 'bg-info';
            prcl2 = 'border-info';
            prtxt = 'Medium priority';
        } else {
            prcl = 'bg-light';
            prcl2 = 'd-none';
        }
        $('#viewModal .modal-header').addClass(prcl).find('h5').text($t.text());
        $('#viewModal .task-priority').addClass(prcl2).text(prtxt);
        bootstrap.Modal.getOrCreateInstance('#viewModal').show();
    });
    
    var taskEdit = $('#editModal');
    taskEdit.on('hidden.bs.modal', function() {
        $f = $(this);
        if ($f.find("input[name='id']").val()) {
            $f.find("form.modal-content")[0].reset();
        }
    });

    $('#editModal form').submit(function( event ) {
        $t = $(this);
        $.ajax({
            method: "POST",
            url: $t.attr('action'),
            data: $t.serialize()
        }).done(function (data) {
            if (data.error) {
                tfk_toasted(data.error, 'text-bg-danger');
            } else if (data.noreload) {
                tfk_toasted(data.success, 'text-bg-success');
            } else {
                // -TODO- better target modals (and review form/node selector as well)
                bootstrap.Modal.getOrCreateInstance('#editModal').hide();
                location.reload();
            }
        });
        event.preventDefault();
    });

    $fss = $('#original-filter-status');
    if ($fss[0]) {
        $fss.clone().prop('id', 'copy-filter-status').appendTo('#search-filter-status');
    }

    $fus = $('#original-filter-users');
    if ($fus[0]) {
        $fus.clone().prop('id', 'copy-filter-users').removeClass('list-group-flush').appendTo('#search-filter-users');
    }

    $('.btn-status label').click(function() {
        $(this).toggleClass('btn-active');
    });

    $('.btn-users label').click(function() {
        $t = $(this);
        if (!$t.hasClass('btn-active')) {
            $t.siblings().removeClass('btn-active');
            $t.toggleClass('btn-active');
        }
    });

});