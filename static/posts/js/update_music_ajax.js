$(document).ready(function() {
  // 검색 버튼 클릭 이벤트 처리
  $("#search-button").click(function() {
    var query = $("#search-input").val(); // 검색어 가져오기
    
    // AJAX 요청
    $.ajax({
      type: "GET",
      url: `/posts/search/`,
      data: { q: query },
      success: function(response) {
        $("#search-results").html(response); // 검색 결과를 결과 영역에 삽입

        // 재생 버튼 클릭 이벤트 처리
        $(".play-track-create").click(function(e) {
          e.preventDefault();
          var audioSrc = $(this).data("src");
          playAudio(audioSrc, 0.3); // 볼륨 조절
        });
      },
      error: function(xhr, status, error) {
        console.log(error); // 에러 처리
      }
    });
  });
  
  // 음악 재생 함수
  function playAudio(src, volume) {
    var audio = $(".music-audio")[0]; // 첫 번째 오디오 요소 가져오기
    audio.src = src;
    audio.volume = volume; // 볼륨 조절
    audio.play();
  }
});