# 오늘, 이음

## 📑목차
- [프로젝트 소개](#🔊프로젝트-소개)
- [팀원](#😎팀원)
- [주요 기능](#✨주요-기능)
- [이슈](#이슈)

## 🔊프로젝트 소개
- 목적 : 밸런스 게임으로 현실과 공감으로 나눠 각각의 성향에 맞는 게시판에서 소통
- 프로젝트 기간 : 23.5.22 ~ 23.6.16
- 발표일 : 23.06.16.
- 팀명 : 13조 위즐, 칙촉🍪
- 주제 : 공감 / 힐링 / 고민
- 개발 동기 : 비슷한 성향의 사람들이 소소하게 대화할 수 있는 공간이 필요

## 😎팀원
- 프론트 : 정미영, 박지현
- 백엔드 : 김용진, 안정환, 장민지 
## ✨주요 기능
1. 밸런스 게임을 통하여 서로의 취향을 분석 후, 유저를 분류  
  <div text-align="center">
    <img src="https://github.com/skysky44/ieum/assets/110805149/60cb87c6-90b6-48d1-8e71-c4ca43c8730e" width="400" height="300"/>    
  </div>
  
<br>

2. 회원가입
  - 이메일 인증  
  <div text-align="center">
    <img src="https://github.com/skysky44/ieum/assets/110805149/b21cabe2-5c7f-4284-b256-ba4dd4a99f12" max-width="800"/>    
  </div>
<br>

3. 취향이 나뉘어진 유저 간 제한 된 게시판에서 취향 공유 등 다양한 게시글 작성  
  - 음악 api를 가져와서 게시글 작성시 음악을 넣고 게시물에 음악 재생
  - ck에디터 활용하여 사진 업로드, 글자 크기 조절, 글씨 색 조정 등
  - 지도 api를 이용하여 유저간 거리 맛집 추천 등 지도 이용
  - 익명 게시판을 통해 모든 유저의 고민 공유 및 댓글 기능으로 공감 / 해결
  - 게시글, 댓글 신고 기능 구현  
  <div text-align="center">
    <img src="https://github.com/skysky44/ieum/assets/110805149/267330c7-bde5-43f5-814c-af210f14bb60" max-width="800"/>  
  </div>
<br>

4. 채팅 기능을 통해 유저끼리 실시간 소통 가능  
  <div text-align="center">
    <img src="https://github.com/skysky44/ieum/assets/110805149/a7b854ce-8d4d-496e-9dbd-016d946d5758" width="400" height="300"/>  
  </div>
<br>
5. 쪽지 기능을 통해 유저끼리 소통  
  <div text-align="center">
    <img src="https://github.com/skysky44/ieum/assets/110805149/58b153d6-2080-4c6b-9161-a5c8aeda1b57" max-width="800"/>  
  </div>
<br>

6. 프로필 페이지에서 상대와 나의 정보 확인
  - 회원가입 시 받은 정보를 토대로 상대와 나의 거리 정보 확인
  - 프로필 뮤직, 사진 설정 가능
  - 회원가입 시 받은 문장이나 밸런스 게임을 통한 단어로 프로필에 '나'를 표현  
  <div text-align="center">
    <img src="https://github.com/skysky44/ieum/assets/110805149/6c01c853-f19d-441a-9c6a-792347a933b0" width="400" height="300"/>  
  </div>
<br>

7. 자바스크립트로 그림판 구현
  - 그림판을 저장하여 수정 가능하며, 이용자 간 그림을 공유하고 자신의 그림을 프로필 이미지로 사용
  <div text-align="center"> 
    <img src="https://github.com/skysky44/ieum/assets/110805149/a1280016-e30e-4d62-9611-19f76c00e54c" width="400" height="300"/>  
  </div>
<br>

8. 모바일 반응형 구현  
  <div text-align="center">
    <img src="https://github.com/skysky44/ieum/assets/110805149/7dc42614-6f53-4645-8c70-16c17fbbb759" width="400" height="300"/>  
  </div>
<br>

9. 클라우드타입, AWS 통한 배포
<br>


## 💥이슈
- Spotify api의 Json데이터를 하나씩 확인하며 원하는 데이터 값을 저장하는데 있어서 시간을 많이 사용함
- 페이지네이션를 AJAX를 사용해 적용시키는 부분에서 시간을 많이 사용함
- 밸런스 게임을 통해 유저를 어떤 기준으로 나눌지에 대해 팀원들끼리 많은 고민을 함
- 밸런스 게임이 정해진 틀이 없었고, 코드를 모두가 이해하기 쉬운 코드로 짜다보니 시간이 오래 걸렸음
- 밸런스 게임을 통해 DB에 저장된 값을 다시 프로필 페이지로 가져와서 체크박스 기능 구현하는데에 어려움을 느낌
- 다양한 필터링 기준을 가지고 유저를 분류해서 게시판을 나누는데 문제 발생
- 채팅 기능 구현(마지막 내용을 입력했을 때와 새로고침하면 스크롤의 위치를 마지막 채팅이 있는 부분으로 이동)
- 채팅 구현 과정에서 메시지를 실시간으로 주고 받는데 어려움(한글 이름 채팅방 생성, 참여자의 프로필 사진 전송 등)
- AWS 배포 시도 중 서버를 생성하고 DB와 연동을 해주는 과정에서의 문제

## ❗느낀점

- 장민지🌹 : 열정을 가진 팀원들 덕에 프로젝트에 애정을 갖고 임할 수 있었습니다. 가장 좋았던 부분은 프로젝트에 들어가기 전에 팀원들과 많은 소통으로 회의시간을 다른 팀보다 길게 가졌습니다. 이 시간 덕에 팀원들의 성향도 알 수 있었고, 프로젝트의 방향성을 잃을 때마다 잘 헤쳐나갈 수 있었습니다. 또한 서로의 코드에 대해 조언을 아끼지 않았고 그런 조언을 받아들이는 멋진 팀원들과 함께 해서 한 달이라는 시간을 뜻깊게 보낼 수 있었습니다!

- 박지현🌷 : 한 달 동안 프로젝트하면서 많이 배웠고 재밌었습니다. 이전에 힘들었던 부분들이 이번에 개발하면서 좀 더 수월하게 진행하게 되어서 뿌듯했습니다. 좋은 팀원 분들과 함께 작업할 수 있어서 즐거웠습니다! 감사합니다!

- 김용진🐲 : 재밌고 웃으면서 할 수 있었던 프로젝트여서 좋은 기억만 남았고 부족한 실력에 대해 서로 피드백 하며 각자의 역량을 키울 수 있는 좋은 기회였고 한달이라는 프로젝트 기간이 빠르게 지나갈 정도로 프로젝트에 진심이었던 조원 분들께 너무나 감사합니다.

- 안정환🌻 : 한달이 길 줄 알았는데, 금방 지나갔네요. 정해진 프로젝트 기간이 이후에도 이어서 작업할 수 있어서 좋았습니다. 다시 보면서 배워가는 것이 많네요. 스스로 부족함을 느끼지만 좋은 팀원들 만나서 얻어가는 것이 많습니다. 친절한 팀원들을 만나 다양한 시도도 해볼 수 있었습니다. 감사합니다!

- 정미영💖 : 회의할 때가 가장 즐거웠던 팀이었어요. 서로의 이야기를 충분히 들어주고 다른 의견도 바로바로 수용할 줄 아시는 따스한 분들을 만나서 힐링하는 팀이었습니다. 게다가 상대방이 기분 나빠하지 않으면서도 의견을 피력하시는 팀원 분 들을 보며 많이 배웠습니다. 더욱 좋았던 점은 성향 분석을 통해서 팀원들과 나의 성향을 하나하나 짚어보며 가까워질 수 있었어요. 그러다 보니 저라는 사람에 대해서도 깊이 생각하게 되더라구요. 이런 좋은 점들을 적용하여 저라는 사람이 최신 버전으로 업데이트되었습니다. 감사합니다!

