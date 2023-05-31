$(document).ready(function() {
  $(".play-music-profile").click(function(e) {
    e.preventDefault();
    var audioSrc = $(this).data("src");
    playAudio(audioSrc);
  });

  function playAudio(src) {
    var audio = $(".music-audio")[0];
    audio.src = src;
    audio.volume = 0.3;
    audio.play();
  }
});