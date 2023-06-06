const likePost = (postid) => {
    btn = document.getElementById('post{{ post.id }}LikesBtn');
    count = document.getElementById('post{{ post.id }}LikesCount');

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