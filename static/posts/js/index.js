// 좋아요 버튼 클릭 시 좋아요 수 +1
// 추후 axios 처리
// const likeBtn = document.querySelector('#like-btn')
// let likeCnt = 0

// likeBtn.addEventListener('click', (event) => {
//     likeCnt += 1
//     const pTag = document.querySelector('#like-cnt')
//     pTag.textContent = likeCnt
//     console.log(pTag.textContent)
// })

// const likeBtn = document.querySelectorAll('.like-btn')
// const forms = document.querySelectorAll('.like-forms')
// const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

// forms.forEach((form) => {
//   form.addEventListener('submit', function (event) {
//     event.preventDefault()
//     const postId = event.target.dataset.postId
//     console.log(postId)
//     // const likeCnt = document.querySelector('#like-count')
//     axios({
//       method:'post',
//       url:`/posts/${postId}/`,
//       headers:{'X-CSRFToken': csrftoken,},
//     })
//     .then((response) => {
//       console.log(response.data.like_count)
//       // likeCnt.textContent = response.data.like_count
//     })
//     .catch((response) => {
//       console.log(error.response)
//     })
//   })
// })

// 안됨
// likeBtn.forEach((like) => {
//   like.addEventListener('submit', function (event) {
//     event.preventDefault()
//     const postId = event.target.dataset.postId
//     console.log(postId)
//     const likeCnt = document.querySelector('.like-count')
//     axios({
//       method:'post',
//       url:`/posts/${postId}/`,
//       headers:{'X-CSRFToken': csrftoken,},
//     })
//     .then((response) => {
//       likeCnt.textContent = response.data.like_count
//       console.log(response.data)
//     })
//     .catch((response) => {
//       console.log(error.response)
//     })
//   })
// })