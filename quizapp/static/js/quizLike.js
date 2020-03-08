// Like or unlike a quiz

let likeBtns = document.querySelectorAll(".quiz__likes_icon");

likeBtns.forEach(item => {
  item.addEventListener("click", function (e) {
    e.preventDefault();

    let url_slug = this.getAttribute("data-slug");
    let like_count = this.parentNode.children[1];

    $.ajax({
      type: "GET",
      url: `api/quiz/like-unlike/`,
      data: {
        slug: url_slug
      },
      success: function (data) {
        if (data.liked) {
          item.classList.add("fas", "liked-heart", "like_animation");
          item.classList.remove("far");
        } else {
          item.classList.add("far");
          item.classList.remove("fas", "liked-heart", "like_animation");
        }
        like_count.innerHTML = `${data.likes}`;
      },
      error: function (err) {
        console.log(err);
      }
    });
  });
});