var checkboxes = document.querySelectorAll('input[name="selected_tracks[]"]');
var saveButton = document.querySelector('.save-button');
var previousCheckbox = null;

function checkSelectedCheckboxes(clickedCheckbox) {
  // 선택된 음원을 제외한 나머지 리스트 숨김 처리
  var selectedTrackId = clickedCheckbox.value;
  var trackItems = document.querySelectorAll('.track-item');
  trackItems.forEach(function(item) {
    var checkbox = item.querySelector('input[type="checkbox"]');
    if (checkbox.value !== selectedTrackId) {
      item.style.display = clickedCheckbox.checked ? 'none' : 'block'; // 체크박스 선택 여부에 따라 리스트 숨김/보임 처리
    }
  });
}

function showAllTracks() {
  var trackItems = document.querySelectorAll('.track-item');
  trackItems.forEach(function(item) {
    item.style.display = 'block'; // 모든 리스트 보이게 처리
  });
}

function toggleCheckbox(clickedTrack) {
  var trackItem = clickedTrack.parentNode;
  var checkbox = trackItem.querySelector('input[type="checkbox"]');

  checkbox.checked = !checkbox.checked; // 체크박스의 상태 반전

  if (!checkbox.checked) {
    previousCheckbox = null;
    showAllTracks(); // 체크박스 선택 해제시 모든 리스트 보이게 처리
  } else {
    checkboxes.forEach(function(checkbox) {
      checkbox.checked = false; // 다른 체크박스 선택 해제
    });
    checkbox.checked = true; // 현재 체크박스 선택
    previousCheckbox = checkbox;
  }

  checkSelectedCheckboxes(checkbox);
}