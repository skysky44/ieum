// 좋아요 버튼 클릭 시 좋아요 수 +1
// 추후 axios 처리
const likeBtn = document.querySelector('#like-btn')
let likeCnt = 0

likeBtn.addEventListener('click', (event) => {
    likeCnt += 1
    const pTag = document.querySelector('#like-cnt')
    pTag.textContent = likeCnt
    console.log(pTag.textContent)
})