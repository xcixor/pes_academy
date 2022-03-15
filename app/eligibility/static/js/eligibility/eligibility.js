$('.fa-solid').on('click', event => {
    $(event.target).toggleClass('fa-angle-right fa-angle-down')
});

$('summary').on('click', event => {
    $(event.target).find('i').toggleClass('fa-angle-right fa-angle-down');
});