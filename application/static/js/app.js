$('document').ready(function(){
  $('.hamburger').click(function() {
    $('.sidebar').toggleClass('show')
  });
  $('.btn-status label').click(function() {
    $(this).toggleClass('btn-active');
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