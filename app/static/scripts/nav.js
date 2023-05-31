const navBar = document.getElementById('nav-container');
const collapseNavBtn = document.getElementById('collapseNavBtn');
const mainContent = document.getElementById('contentMain');
const linksText = document.getElementsByClassName('links-text');
const navLinks = document.getElementById('navLinks');
const navName = document.getElementById('navName');
const collapseNavIcon = document.getElementById('collapseNavIcon');

collapseNavBtn.addEventListener('click', () => {

    if (navBar.classList.contains('nav-container-small') && mainContent.classList.contains('main-content-large')) {
        navBar.classList.remove('nav-container-small');
        mainContent.classList.remove('main-content-large');
        navLinks.classList.remove('links-small');
        navName.classList.remove('hide');
        collapseNavIcon.classList.remove('collapseNavIconFront');
        collapseNavIcon.classList.add('collapseNavIconBack')

        for (let i = 0; i < linksText.length; i++) {
            linksText[i].classList.remove('hide');
        }
    }
    else {
        navBar.classList.add('nav-container-small');
        mainContent.classList.add('main-content-large');
        navLinks.classList.add('links-small');
        navName.classList.add('hide');
        collapseNavIcon.classList.add('collapseNavIconFront');
        collapseNavIcon.classList.remove('collapseNavIconBack')

        for (let i = 0; i < linksText.length; i++) {
            linksText[i].classList.add('hide');
        }
    }
})