const likePost = (postid) => {
    btn = document.getElementById(`post${ postid }LikesBtn`);
    count = document.getElementById(`post${ postid }LikesCount`);

    fetch(`/post/like/${postid}`, {method:'POST'}).then((res) => res.json()).then((data) => {
        count.innerText = data['likes'];
        
        if (data['liked'] == true) {
            btn.classList.add('like-active');
        }
        else {
            btn.classList.remove('like-active');
        }
    })
    .catch((e) => alert('ERROR: Post cannot be liked'));
}