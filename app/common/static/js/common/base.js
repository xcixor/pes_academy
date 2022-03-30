$('#languageSelect').on('change', function (){
  console.log('submitted');
  $('#languageForm').submit();
});


$('#closeMessagesContainer').on('click', function(){
    console.log('close');
    // setTimeout(function() {
    //     $('.alert-container').css({'display': 'none !important'});
    // }, 200);
    // $('.alert').css({'display': 'none !important'});
});

// $(document).ready(function(){
//     $('[data-toggle="offcanvas"]').click(function(){
//         $("#navigation").toggleClass("hidden-xs");
//     });
//  });

 function openPage(pageName,elmnt,color) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].style.backgroundColor = "none";
    }
    document.getElementById(pageName).style.display = "block";
    elmnt.style.backgroundColor = color;
  }

  // Get the element with id="defaultOpen" and click on it
  document.getElementById("defaultOpen").click();


document.querySelector("#show-form").addEventListener("click", function(){
  document.querySelector(".popup").classList.add("active");
});

document.querySelector(".popup .close-btn").addEventListener("click",function(){
  document.querySelector(".popup").classList.remove("active");
});
