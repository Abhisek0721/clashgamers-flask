
let Toggle = document.getElementById('toggle');
let mobileNavList = document.querySelector(".nav-list");
let toggleBars = document.querySelectorAll('.toggle span');


function responsiveEffect() {
    if (window.innerWidth < 950) {
        document.body.classList.add('mobile');
    } else {
        document.body.classList.remove('mobile');
    };
};

window.onload = responsiveEffect();

window.addEventListener('resize', () => {
    responsiveEffect();
});

let switchToggle = 'off';

Toggle.addEventListener('click', function() {
    mobileNavList.classList.toggle('open');

    if (switchToggle == 'off') {
        toggleBars[0].style.transform = 'rotate(45deg)';
        toggleBars[1].style.opacity = '0';
        toggleBars[2].style.transform = 'rotate(-45deg)';
        switchToggle = 'on';
    } else {
        toggleBars[0].style.transform = 'rotate(0deg)';
        toggleBars[1].style.opacity = '1';
        toggleBars[2].style.transform = 'rotate(0deg)';
        switchToggle = 'off';
    }

});