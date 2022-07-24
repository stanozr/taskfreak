$('document').ready(function(){

    var taskView = $('#viewModal');
    if (taskView[0]) {
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
        new bootstrap.Modal('#viewModal').show();
      });
    }
    
});