$(window).on('load', function () {
	let stepNumber = localStorage.getItem("stepNumber");
    if ( !stepNumber ) {
        navigateToFormStep(parseInt(1));

      }else{
        navigateToFormStep(parseInt(stepNumber));

      }
});

$('.fa-solid').on('click', event => {
    $(event.target).toggleClass('fa-angle-right fa-angle-down')
});

$('summary').on('click', event => {
    $(event.target).find('i').toggleClass('fa-angle-right fa-angle-down');
});
