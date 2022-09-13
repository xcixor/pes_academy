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

  const countdown = document.querySelector('.countdown');

// Set Launch Date (ms)
const launchDate = new Date('Sep 26, 2022 12:00:00').getTime();

// Update every second
const intvl = setInterval(() => {
  // Get todays date and time (ms)
  const now = new Date().getTime();

  // Distance from now and the launch date (ms)
  const distance = launchDate - now;

  // Time calculation
  const days = Math.floor(distance / (1000 * 60 * 60 * 24));
  const hours = Math.floor(
    (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
  );
  const mins = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display result
  countdown.innerHTML = `
  <div>${days}<span>Days</span></div> 
  <div>${hours}<span>Hours</span></div>
  <div>${mins}<span>Minutes</span></div>
  <div>${seconds}<span>Seconds</span></div>
  `;

  // If launch date is reached
  if (distance < 0) {
    // Stop countdown
    clearInterval(intvl);
    // Style and output text
    countdown.style.color = '#17a2b8';
    countdown.innerHTML = 'Launched!';
  }
}, 1000);

});


