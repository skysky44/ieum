// 셀렉트 변경 시 처리
document.getElementById("comment-select").addEventListener("change", function () {
  var selectedOption = this.value;

  // 선택한 옵션에 따라 댓글 섹션 변경
  if (selectedOption === "comments") {
    document.getElementById("comments-section").classList.remove("comments-hidden");
    document.getElementById("latest-comments-section").classList.add("comments-hidden");
  } else if (selectedOption === "latest-comments") {
    document.getElementById("comments-section").classList.add("comments-hidden");
    document.getElementById("latest-comments-section").classList.remove("comments-hidden");
  }
});


document.addEventListener("DOMContentLoaded", function() {
  var latestCommentSection = document.getElementById("latest-comments-section");
  var latestLoadMoreBtn = latestCommentSection.querySelector(".load-more-comments");
  var latestComments = latestCommentSection.getElementsByClassName("latest-comment");
  var latestCommentsToShow = 5;
  var latestCommentsLoaded = latestCommentsToShow;
  var oldCommentSection = document.getElementById("comments-section");
  var oldLoadMoreBtn = oldCommentSection.querySelector(".load-more-comments");
  var oldComments = oldCommentSection.getElementsByClassName("old-comment");
  var oldCommentsToShow = 5;
  var oldCommentsLoaded = oldCommentsToShow;

  // 초기에 댓글을 숨김
  hideComments(latestComments, latestCommentsToShow);
  hideComments(oldComments, oldCommentsToShow);

  // 기본적으로 5개의 댓글을 보여줌
  showMoreComments(latestComments, 0, latestCommentsToShow);
  showMoreComments(oldComments, 0, oldCommentsToShow);

  // 최신 댓글 더보기 버튼 클릭 시 추가 댓글 로드
  latestLoadMoreBtn.addEventListener("click", function() {
    showMoreComments(latestComments, latestCommentsLoaded, latestCommentsToShow);
    latestCommentsLoaded += latestCommentsToShow;

    if (latestCommentsLoaded >= latestComments.length) {
      latestLoadMoreBtn.style.display = "none";
    }
  });

  // 오래된 댓글 더보기 버튼 클릭 시 추가 댓글 로드
  oldLoadMoreBtn.addEventListener("click", function() {
    showMoreComments(oldComments, oldCommentsLoaded, oldCommentsToShow);
    oldCommentsLoaded += oldCommentsToShow;

    if (oldCommentsLoaded >= oldComments.length) {
      oldLoadMoreBtn.style.display = "none";
    }
  });

  // 댓글 숨김 및 추가 노출 함수
  function hideComments(comments, commentsToShow) {
    for (var i = commentsToShow; i < comments.length; i++) {
      comments[i].style.display = "none";
    }
  }

  function showMoreComments(comments, commentsLoaded, commentsToShow) {
    for (var i = commentsLoaded; i < commentsLoaded + commentsToShow; i++) {
      if (i < comments.length) {
        comments[i].style.display = "block";
      }
    }
  }
});