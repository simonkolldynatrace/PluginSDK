(function(){
  var cc2 = $('#search');
  var ii2 = $('.search-input');

  $('body').on('click', () =>  ii2.removeClass('focus'));
  cc2.on('click', (e) => e.stopPropagation());

  $('label[for*=search-input]').on('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    ii2.addClass('focus');
    ii2.focus();
  });

  $(document).on('keyup', (e) => {
    if(e.keyCode === 27) {
      ii2.removeClass('focus');
    }
  });
})();


