// PARTNERS JS
$(document).ready(function() {
  const mainNav = document.querySelector('.main-nav');
const hamburgerMenu = document.querySelector('.hamburger-menu');
hamburgerMenu.addEventListener('click',() => {
     mainNav.classList.toggle('open');
});
gsap.fromTo('.hero-clipped',{scaleX: 0},{duration: 1,scaleX: 1});
gsap.fromTo('.logo',{x: 200,opacity: 0},{duration: 1,delay: 0.5,x: 0,opacity: 1});
gsap.fromTo('.hamburger-menu',{x: 200,opacity: 0},{duration: 1,delay: 0.8,x: 0,opacity: 1});
gsap.fromTo('.hero-textbox',{yPercent: 40,opacity: 0},{duration: 1,delay: 1.3,yPercent: -50,opacity: 1});


  $('.section').hover(function() {
    var $this = $(this);
    if ($this.hasClass("show-desc")) {
       $this.find('div.cover').css({top: "0"});
       $this.find('div.desc').css({top: "100%"});
       $this.find('[class*="entypo-"]').removeClass('spin-out').addClass('spin-in');
      $this.find('.cover h5').addClass('scoot-in');
       $this.removeClass("show-desc");
    }
    else {
       $this.find('div.cover').css({top: "-100%"});
       $this.find('div.desc').css({top: "0"});
       $this.find('[class*="entypo-"]').removeClass('spin-in').addClass('spin-out');
       $this.find('.cover h5').removeClass('scoot-in').addClass('scoot-out');
       $this.addClass("show-desc");
    }
  });
});


