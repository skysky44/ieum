// document.addEventListener('DOMContentLoaded', function() {
//   var audioPlayer = document.getElementById('audio-player');
//   var playLinks = document.querySelectorAll('.play-track');

//   playLinks.forEach(function(link) {
//     link.addEventListener('click', function(e) {
//       e.preventDefault();

//       var audioSrc = this.getAttribute('data-src');
//       audioPlayer.setAttribute('src', audioSrc);
//       audioPlayer.play();

//       // 선택한 노래를 제외한 나머지 리스트 숨김
//       var selectedTrackId = this.parentNode.id;
//       var trackList = document.getElementsByTagName('li');
//       for (var i = 0; i < trackList.length; i++) {
//         if (trackList[i].id !== selectedTrackId) {
//           trackList[i].style.display = 'none';
//         }
//       }
//     });
//   });
// });

document.addEventListener('DOMContentLoaded', function() {
  var audioPlayer = document.getElementById('audio-player');
  // 오디오 볼륨 0.3으로 설정
  audioPlayer.volume = 0.3;

  // 이벤트 위임을 활용하여 play-track 클래스를 가진 요소들에 대한 이벤트 처리
  document.addEventListener('click', function(event) {
      var target = event.target;

      if (target.classList.contains('play-track')) {
          event.preventDefault();

          var audioSrc = target.getAttribute('data-src');
          audioPlayer.setAttribute('src', audioSrc);
          audioPlayer.load();
          audioPlayer.play();
      }

    if (target.classList.contains('save-button')) {
      var trackId = target.parentNode.getAttribute('data-track-id');
      var form = document.querySelector('form[action="' + "{% url 'accounts:save_track' %}" + '"]');
      var actionUrl = form.getAttribute('action');
      actionUrl += trackId;
      form.setAttribute('action', actionUrl);
      form.submit();
    }
  });
});