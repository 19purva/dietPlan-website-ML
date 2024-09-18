// script.js
document.querySelector('.hamburger').addEventListener('click', () => {
    document.querySelector('.nav-links').classList.toggle('nav-active');
    document.querySelector('.search-bar').classList.toggle('nav-active');
});
