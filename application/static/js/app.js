$('document').ready(function(){

  var taskView = $('#viewModal');
  if (taskView[0]) {
    taskView.on('hidden.bs.modal', function() {
      $(this).find('.modal-header').removeClass('bg-danger bg-warning bg-info bg-light text-light');
    });
    $('.task-title').click(function() {
      $t = $(this);
      prcl = '';
      prio = $t.closest('.task-row').find('.task-deadline');
      if (prio.hasClass('priority-3')) {
        prcl = 'bg-danger text-light';
      } else if (prio.hasClass('priority-2')) {
        prcl = 'bg-warning';
      } else if (prio.hasClass('priority-1')) {
        prcl = 'bg-info';
      } else {
        prcl = 'bg-light';
      }
      $('#viewModal .modal-header').addClass(prcl).find('h5').text($t.text());
      new bootstrap.Modal('#viewModal').show();
    });
  }

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

  $('.hamburger').click(function() {
    $('.sidebar').toggleClass('show')
  });

  $('.dropdown-item').click(function(e) {
    if (e.target === e.currentTarget) {
      $(this).children('input').click();
    }
  });

  $(".dropdown input[type='checkbox']").change(function() {
    $p = $(this).closest('.dropdown');
    $c = $p.find("input[type='checkbox']");
    var t = 0;
    $c.each(function( index ) {
      if ($(this).prop( "checked" )) {
        t += 1;
      }
    });
    $p.find('.dropdown-count').text(t);
  })

  $('.datepicker').datepicker();
});