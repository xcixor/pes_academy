$('#languageSelect').on('change', function (){
  console.log('submitted');
  $('#languageForm').submit();
});


/*FAQ Page*/

// Toggle Form Visibility

const btn = document.getElementById('help-form-btn');

btn.addEventListener('click', () => {
  const form = document.getElementById('help-form');

  if (form.style.display === 'none') {
    // 👇️ this SHOWS the form
    form.style.display = 'block';
  } else {
    // 👇️ this HIDES the form
    form.style.display = 'none';
  }
});


var accordWithPage =  function() {
  
  var faqDiv = $('#faq-links div');
   
 
 $(function () {
   
 faqDiv.click(function() {
     
   var hideSec = 'faq-hide';  
       var $this = $(this),
       $id = $this.attr('id'),
       $class = '.' + $('.about-' + $id).attr('class').replace(hideSec, '');
 
   $('#faq-wrapper').addClass(hideSec);
   $('.about-' + $id).removeClass(hideSec);
   $('div[class*=about]').not($class).addClass(hideSec);
      
  });
 
 });
 
 $(function () {
   
         var select = 'faq-selected';      
   
         faqDiv.click(function () {
 
         if ($(this).hasClass(select)) {
             $(this).removeClass(select);
         } else {
             $('#faq-links .faq-selected').removeClass(select);
             $(this).addClass(select);             
         }
     }); //faq link selected
 });
 
   
   
 //Accordion
   
 $(function () {
   
   var expand = 'expanded';
   var content = $('.faq-content');
         //FAQ Accordion
         $('.faq-accordion > li > a').click(function (e) {
             e.preventDefault();
         if ($(this).hasClass(expand)) {
             $(this).removeClass(expand);
 //          $('.faq-accordion > li > a > div').not(this).css('opacity', '1');//returns li back to normal state
             $(this).parent().children('ul').stop(true, true).slideUp();
         } else {
 //            $('.faq-accordion > li > a > div').not(this).css('opacity', '0.5');//dims inactive li
             $('.faq-accordion > li > a.expanded').removeClass(expand);
             $(this).addClass(expand);
             content.filter(":visible").slideUp();
             $(this).parent().children('ul').stop(true, true).slideDown();
         }
     }); //accordion function
 
     content.hide();
 
 }); 
   
 }
 
 accordWithPage();
 
 /*$(function () {
    $("#faq-links div").click(function () {
     $('.slide-left').fadeOut( "slow", "linear" );
      $('.slide-left').fadeIn( "slow", "linear" );
     }); //faq link fade in and out
   }); //document ready*/
