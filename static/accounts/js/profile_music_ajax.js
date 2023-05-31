$(document).ready(function() {
  // 검색 폼이 제출되면 Ajax 요청을 보냅니다.
  $('#search-form').on('submit', function(event) {
    event.preventDefault();
    var query = $('#search-input').val();

    $.ajax({
      type: 'GET',
      url: '/accounts/search/',
      data: { q: query },
      success: function(response) {
        $('#search-results').html(response);
      },
      error: function(xhr, status, error) {
        console.log('오류:', error);
      }
    });
  });
});