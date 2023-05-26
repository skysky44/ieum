document.addEventListener('DOMContentLoaded', function() {
  var audioPlayer = document.getElementById('audio-player');
  var playLinks = document.querySelectorAll('.play-track');

  playLinks.forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();

      var audioSrc = this.getAttribute('data-src');
      audioPlayer.setAttribute('src', audioSrc);
      audioPlayer.play();

      // 선택한 노래를 제외한 나머지 리스트 숨김
      var selectedTrackId = this.parentNode.id;
      var trackList = document.getElementsByTagName('li');
      for (var i = 0; i < trackList.length; i++) {
        if (trackList[i].id !== selectedTrackId) {
          trackList[i].style.display = 'none';
        }
      }
    });
  });
});