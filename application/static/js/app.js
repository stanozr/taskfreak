$('document').ready(function(){

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
  });

  $('.flash').each(function() {
    new bootstrap.Toast($(this)).show();
  });

  confirmModal = new bootstrap.Modal('#confirmModal');

  $( "#confirmModal form" ).submit(function( event ) {
    $t = $(this);
    $.ajax({
        method: $t.attr('method'),
        url: $t.attr('action'),
        data: $t.serialize()
    }).done(function (data) {
        if (data.error) {
            tfk_toasted(data.error, 'text-bg-danger');
        } else {
          confirmModal.hide();
          location.reload();
        }
    });
    event.preventDefault();
  });

  $("a[data-tfk-ajax]").click(function(event) {
    $t = $(this);
    event.preventDefault();
    $.ajax({
      method: $t.data('tfk-ajax'),
      url: $t.attr('href')
    }).done(function (data) {
      if (data.error) {
          tfk_toasted(data.error, 'text-bg-danger');
      } else {
        confirmModal.hide();
        location.reload();
      }
    });
  });

  $("a[data-tfk-confirm]").click(function(event) {
    $t = $(this);
    event.preventDefault();
    tfk_confirm($t.data('tfk-confirm'), $t.attr('href'));
  });

  $("button[data-tfk-confirm]").click(function(event) {
    $t = $(this);
    event.preventDefault();
    tfk_confirm($t.data('tfk-confirm'), $t.data('tfk-action'));
  })

  $('.datepicker').datepicker({
    format: 'dd/mm/yyyy',
  });

});

function tfk_confirm(msg, action) {
  $mod = $('#confirmModal');
  $mod.find('.modal-body').html(msg);
  $mod.find('form').attr('action', action);
  confirmModal.show();
}

function tfk_toasted(msg, cat) {
  $lt = $('#live-toast');
  $lt.addClass(cat).find('.toast-body').text(msg);
  mt = bootstrap.Toast.getOrCreateInstance($lt);
  $lt.on('hidden.bs.toast', () => {
    $lt.removeClass('text-bg-danger text-bg-warning text-bg-success text-bg-info');
  })
  mt.show();
}