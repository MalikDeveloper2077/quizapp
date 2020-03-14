// Show modal and delete a quiz

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
let csrf_token = $('input[name=csrfmiddlewaretoken]').val();

$(document).on('submit', '#delete__form', function(e) {
    e.preventDefault();

    $.ajax({
        type: 'DELETE',
        url: `/api/quiz/${slug}/delete/`,
        data: {},
        headers:{"X-CSRFToken": csrf_token},
        success: function(data) {
            if ( window.location.href.includes('quiz/') ) {
                window.location.replace('/')
            } else {
                quiz.style.display = 'none';
            }
        },
        error: function(error) {
            console.log('error')
        }
    })
})
