//Add your script

$(document).ready(function() {
  
  $('footer a').first().click(function() {
    $(window)[0].menu.close();
  });
  
  $('.rooms-list__type-text').html('Canais');
});