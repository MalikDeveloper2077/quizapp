let modal = document.querySelector('.modal');
let btns = document.querySelectorAll('.list__item_delete');
let close = document.querySelector('.modal__close');
let submitBtn = document.querySelector('.modal__btn_delete');
let slug;
let quiz;

btns.forEach(function(item) {
    item.addEventListener('click', function() {
        modal.style.display = 'flex';
        slug = item.getAttribute('data-slug');
        quiz = item.parentNode.parentNode.parentNode.parentNode.parentNode
    })
})

submitBtn.addEventListener('click', function() {
    modal.style.display = 'none';
})

close.addEventListener('click', function() {
    modal.style.display = 'none';
})

window.onclick = function(e) {
    if (e.target == modal) {
        modal.style.display = "none";
    }
}

// Ajax to delete the quiz
let btn = document.querySelector('.modal__btn_delete');

btn.addEventListener('click', function(e) {
    e.preventDefault();

    $.ajax({
        type: 'GET',
        url: `api/quiz/delete/${slug}/`,
        data: {},
        success: function(data) {
            quiz.style.display = 'none';
        },
        error: function(error) {
            console.log('error')
        }
    })
})
