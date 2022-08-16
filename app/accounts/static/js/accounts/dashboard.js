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
    // elmnt.style.backgroundColor = color;
  }

  // Get the element with id="defaultOpen" and click on it
  document.getElementById("defaultOpen").click();


document.querySelector("#show-form").addEventListener("click", function(){
  document.querySelector(".popup").classList.add("active");
});

document.querySelector(".popup .close-btn").addEventListener("click",function(){
  document.querySelector(".popup").classList.remove("active");
});

$('#sideNavIcon').on('click', ()=> {
  $('#navigation').toggle({ direction: "right" }, 1000);
  $('#navigation').addClass("toggle-click");
});

$('#closeSideNav').on('click', ()=>{
  $('#navigation').toggle({ direction: "right" }, 10000);
});

$(".toggle-click").on('click', ()=> {
  $('#navigation').css('display', 'none');
});

$(document).on('click', ".toggle-click", function() {
      $('#navigation').css('display', 'none');

});