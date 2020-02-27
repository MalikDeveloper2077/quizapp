// Show manage menu when mouse is over .manage__menu icon

let menu = document.querySelectorAll('.manage__menu');

menu.forEach(item => {
    item.addEventListener('mouseenter', function(e) {
        let menuUl = this.parentNode.children[1];
        menuUl.classList.add('show');

        // Hide manage menu
        menuUl.addEventListener('mouseleave', function(e) {
            this.classList.remove('show');
        })
    })
})
