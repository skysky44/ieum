// 최신댓글 좋아요
const form = document.querySelectorAll('[id^="comment-like-form-"]');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

form.forEach(function (form) {
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const postId = event.target.dataset.postId;
    const commentId = event.target.dataset.commentId;

    axios({
      method: 'post',
      url: `/posts/${postId}/comments/${commentId}/comment_likes/`,
      headers: {'X-CSRFToken': csrftoken},
    })
    .then((response) => {
      const o_form = document.querySelector(`#comment-like-o-form-${commentId}`);
      const commentLike = response.data.liked;
      const heartButton = form.querySelector('#comment-heart');
      const heartButton2 = o_form.querySelector('#comment-heart-2');
      const commentCountTag = form.querySelector('#comment-like-count');
      const commentCountTag2 = o_form.querySelector('#comment-like-count-2');

      if (commentLike) {
        heartButton.textContent = "❤️";
        heartButton2.textContent = "❤️";
      } else {
        heartButton.textContent = "🤍";  
        heartButton2.textContent = "🤍";  
      }

      const commentCountData = response.data.like_count;
      commentCountTag.textContent = commentCountData;
      commentCountTag2.textContent = commentCountData;
    })
    .catch((error) => {
      console.log(error);
    });
  });
});

// 오래된댓글 좋아요
const form2 = document.querySelectorAll('[id^="comment-like-o-form-"]');
form2.forEach(function (form) {
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const postId = event.target.dataset.postId;
    const commentId = event.target.dataset.commentId;

    axios({
      method: 'post',
      url: `/posts/${postId}/comments/${commentId}/comment_likes/`,
      headers: {'X-CSRFToken': csrftoken},
    })
    .then((response) => {
      const l_form = document.querySelector(`#comment-like-form-${commentId}`);
      const heartButton = l_form.querySelector('#comment-heart');
      const heartButton2 = form.querySelector('#comment-heart-2');
      const commentCountTag = l_form.querySelector('#comment-like-count');
      const commentCountTag2 = form.querySelector('#comment-like-count-2');
      const commentLike = response.data.liked;

      if (commentLike) {
        heartButton.textContent = "❤️";
        heartButton2.textContent = "❤️";
      } else {
        heartButton.textContent = "🤍";  
        heartButton2.textContent = "🤍";  
      }

      const commentCountData = response.data.like_count;
      commentCountTag.textContent = commentCountData;
      commentCountTag2.textContent = commentCountData;
    })
    .catch((error) => {
      console.log(error);
    });
  });
});