$(document).ready(function() {
  // 드롭다운 선택 이벤트 리스너
  $('#section-dropdown').on('change', function() {
    var selectedSection = $(this).val();
    var currentPage = 1; // 첫 페이지로 설정
    var url = '/posts/';
    // AJAX 요청 전송
    sendAjaxRequest(url, selectedSection, currentPage);
  });


  // AJAX 요청 전송 함수
  function sendAjaxRequest(url, section, page) {
    $.ajax({
      url: url,
      method: 'GET',
      data: { section: section, page: page },
      success: function(response) {
        // 서버로부터 받은 HTML을 section-posts 영역에 대체
        $('#section-posts').html($(response).find('#section-posts').html());
        // 선택된 섹션을 유지하기 위해 드롭다운 값을 설정
        $('#section-dropdown').val(section);
        // 현재 페이지 데이터 속성 업데이트
        $('#section-posts').data('current-page', page);
        updatePagination(); // 페이지네이션 업데이트
      }
    });
  }

  // 페이지네이션 업데이트 함수
  function updatePagination() {
    var currentPage = parseInt($('#section-posts').data('current-page')) || 1;
    var total_pages = parseInt('{{ total_pages }}') || 1;
    var pageLinks = $('.page-link');
    pageLinks.parent('.page-item').removeClass('active');

    // 현재 페이지 버튼에 active 클래스 추가
    pageLinks.each(function() {
      var pageNumber = $(this).attr('href').split('=')[1];
      if (pageNumber == currentPage) {
        $(this).parent('.page-item').addClass('active');
      }
    });

    // 페이지 범위 설정
    var pageRange = 5; // 출력할 페이지 범위 크기
    var startPage = Math.max(1, currentPage - Math.floor(pageRange / 2));
    var endPage = Math.min(total_pages, startPage + pageRange - 1);
    startPage = Math.max(1, endPage - pageRange + 1);

    // 페이지 버튼 업데이트
    var paginationContainer = $('.pagination');
    paginationContainer.empty();

    // 첫 페이지와 이전 페이지 버튼
    if (currentPage > 1) {
      paginationContainer.append('<li class="page-item first-page"><a class="page-link" href="?page=1">처음</a></li>');
      paginationContainer.append('<li class="page-item previous-page"><a class="page-link" href="?page=' + (currentPage - 1) + '">이전</a></li>');
    }

    // 페이지 버튼
    for (var i = startPage; i <= endPage; i++) {
      if (i == currentPage) {
        paginationContainer.append('<li class="page-item active"><a class="page-link" href="?page=' + i + '">' + i + '</a></li>');
      } else {
        paginationContainer.append('<li class="page-item"><a class="page-link" href="?page=' + i + '">' + i + '</a></li>');
      }
    }

    // 다음 페이지와 마지막 페이지 버튼
    if (currentPage < total_pages) {
      paginationContainer.append('<li class="page-item next-page"><a class="page-link" href="?page=' + (currentPage + 1) + '">다음</a></li>');
      paginationContainer.append('<li class="page-item last-page"><a class="page-link" href="?page=' + total_pages + '">마지막</a></li>');
    }
  }
});