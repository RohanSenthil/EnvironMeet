const likePost = (postid) => {
    btn = document.getElementById(`post${ postid }LikesBtn`);
    count = document.getElementById(`post${ postid }LikesCount`);

    const csrfTokenElem= document.getElementById(`post${ postid }Likes`).querySelector('input[name="csrf_token"]');

    if (csrfTokenElem) {
        csrfToken = csrfTokenElem.value
    } 
    else {
        csrfToken = null
    }

    fetch(`/post/like/${postid}`, {method:'POST', headers: {'X-CSRFToken': csrfToken}}).then((res) => res.json()).then((data) => {
        count.textContent = data['likes'];
        
        if (data['liked'] == true) {
            btn.classList.add('like-active');
        }
        else {
            btn.classList.remove('like-active');
        }
    })
    .catch((e) => alert('ERROR: Post cannot be liked'));
}