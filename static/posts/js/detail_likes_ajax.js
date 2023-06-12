  // Function to handle the like button click event
  async function handleLike(event) {
    event.preventDefault(); // Prevent the default form submission

    const form = event.target; // Get the form element
    const postId = form.getAttribute("data-post-id"); // Get the post ID

    try {
      const response = await fetch(`/posts/${postId}/likes/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"), // Get CSRF token from cookie
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      const data = await response.json(); // Parse the JSON response

      // Update the like button and count based on the server response
      const likeButton = form.querySelector("button");
      const likeCount = document.getElementById("like-count");

      if (data.is_liked) {
        likeButton.innerHTML = `
          <i class="bi bi-hand-thumbs-up text-primary" style="font-size:1.5rem;"></i>
        `;
        likeButton.setAttribute("value", "좋아요");
      } else {
        likeButton.innerHTML = `
          <i class="bi bi-hand-thumbs-up text-secondary" style="font-size:1.5rem;"></i>
        `;
        likeButton.setAttribute("value", "좋아요 취소");
      }

      likeCount.innerHTML = data.like_count;
    } catch (error) {
      console.error(error);
    }
  }

  // Attach the click event listener to the like form
  const likeForms = document.getElementsByClassName("like-form");
  for (const form of likeForms) {
    form.addEventListener("submit", handleLike);
  }

  // Function to get CSRF token from cookie
  function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
  }