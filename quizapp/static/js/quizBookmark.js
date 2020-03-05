// Like or unlike a quiz

let bookmarkBtns = document.querySelectorAll('.quiz__bookmarks_icon');

bookmarkBtns.forEach(item => {
  item.addEventListener('click', function(e) {
    e.preventDefault();

    let url_slug = this.getAttribute('data-slug')
    let bookmarks_count = this.parentNode.children[1]
    let csrf_token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
      type: 'POST',
      url: `api/quiz/bookmark/create-remove/`,
      data: {
        slug: url_slug
      },
      headers:{"X-CSRFToken": csrf_token},
      success: function(data) {
        console.log(data);
        if (data.bookmarked) {
          item.classList.remove('far')
          item.classList.add('fas', 'bookmarked', 'bookmark_animation');
        } else {
          item.classList.add('far')
          item.classList.remove('fas', 'bookmarked', 'bookmark_animation');
        }
        bookmarks_count.innerHTML = `${data.bookmarks}`;
      },
      error: function(err) {
        console.log(err);
      }
    })
  })
})
