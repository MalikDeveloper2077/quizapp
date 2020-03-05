// Delete a quiz comment

$(document).on('submit', '#delete__form', function(e) {
    e.preventDefault();

    let form = this;
    let pk = form.getAttribute('data-pk');
    let csrf_token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        type: 'DELETE',
        url: `/api/quiz/comment/delete/${pk}`,
        data: {},
        headers:{"X-CSRFToken": csrf_token},
        success: function(data) {
            form.parentNode.parentNode.style.display = 'none';
        },
        error: function(err) {
            console.log(err)
        }
    })
})
