$('#closeMessagesContainer').on('click', function(){
    console.log('close');
    // setTimeout(function() {
    //     $('.alert-container').css({'display': 'none !important'});
    // }, 200);
    // $('.alert').css({'display': 'none !important'});
});

$(document).ready(function(){
    $('[data-toggle="offcanvas"]').click(function(){
        $("#navigation").toggleClass("hidden-xs");
    });
 });