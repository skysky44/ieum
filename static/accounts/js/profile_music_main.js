document.addEventListener('DOMContentLoaded', function() {
  var audioPlayer = document.getElementById('audio-player');
  var mainAudioPlayer = document.querySelector('.main-audio');
  var playTrackButtons = document.querySelectorAll('.play-track');
  var playTrackProfileButtons = document.querySelectorAll('.play-track-profile');

  // 오디오 볼륨 0.3으로 설정
  audioPlayer.volume = 0.3;
  mainAudioPlayer.volume = 0.3;

  // 이벤트 위임을 활용하여 play-track 클래스를 가진 요소들에 대한 이벤트 처리
  document.addEventListener('click', function(event) {
    var target = event.target;

    if (target.classList.contains('play-track')) {
      event.preventDefault();

      var audioSrc = target.getAttribute('data-src');
      audioPlayer.setAttribute('src', audioSrc);
      audioPlayer.load();
      audioPlayer.play();

      // 다른 쪽 오디오 플레이어 멈춤
      mainAudioPlayer.pause();
      mainAudioPlayer.currentTime = 0;
    } else if (target.classList.contains('play-track-profile')) {
      event.preventDefault();

      var audioSrc = target.getAttribute('data-src');
      mainAudioPlayer.setAttribute('src', audioSrc);
      mainAudioPlayer.load();
      mainAudioPlayer.play();

      // 다른 쪽 오디오 플레이어 멈춤
      audioPlayer.pause();
      audioPlayer.currentTime = 0;
    }
  });
});