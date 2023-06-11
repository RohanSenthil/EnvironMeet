const addComment = (postid) => {
    let searchData = new URLSearchParams();
    searchData.append('desc', document.getElementById(`commentInput-${postid}`).value);

    fetch(`/post/comment/add/${postid}`, {method: 'POST', 
    body: searchData}).then((res) => res.json())
    .then((data) => { 
        if (data['success']) {
            const commentDiv = document.getElementById(`form-reload-${data['postid']}`);

            $(commentDiv).load(document.URL + ' ' + `#form-reload-${data['postid']}`);
        }

    })
    .catch((e) => alert('ERROR: This comment cannot be posted'));

    return false;
}


const editComment = (commentid) => {
    let searchData = new URLSearchParams();
    searchData.append('desc', document.getElementById(`editCommentInput-${commentid}`).value);

    const editModal = document.getElementById(`editCommentModal_${commentid}`)
    $(editModal).modal('hide');

    fetch(`/post/comment/edit/${commentid}`, {method: 'POST', 
    body: searchData}).then((res) => res.json())
    .then((data) => { 
        if (data['success']) {
            const commentDiv = document.getElementById(`form-reload-${data['postid']}`);

            $(commentDiv).load(document.URL + ' ' + `#form-reload-${data['postid']}`);
        }

    })
    .catch((e) => alert('ERROR: This comment cannot be posted'));
}


const deleteComment = (commentid) => {
    const deleteItem = document.getElementById(`commentText-${commentid}`);
    const deleteModal = document.getElementById(`deleteCommentModal_${commentid}`)

    $(deleteModal).modal('hide');

    fetch(`/post/comment/delete/${commentid}`, {method: 'POST'}).then((res) => res.json())
    .then((data) => { 
        if (data['success']) {
            const parentBox = document.getElementById(`commentSection-${data['postid']}`);
            $(deleteItem).remove();
            $(parentBox).load(document.URL + ' ' + `#commentSection-${data['postid']}`);
        }
    })
    .catch((e) => alert('ERROR: This comment cannot be deleted'));
}


const updateItemsVisbility = (postid, commentsToShow) => {
    let commentsContainer = document.getElementById(`commentSection-${postid}`);
    let comments = commentsContainer.getElementsByClassName('comments');

    for (let i = 0; i < comments.length; i++) {
        if (i < commentsToShow) {
            comments[i].style.display = 'flex';
        } else {
            comments[i].style.display = 'none';
        }
    }

    let moreBtn = document.getElementById(`moreComments-${postid}`);
    let lessBtn = document.getElementById(`lessComments-${postid}`);

    if (commentsToShow <= 3) {
        lessBtn.style.display = 'none';
    } else {
        lessBtn.style.display = 'block';
    }
    
    if (commentsToShow >= comments.length) {
        moreBtn.style.display = 'none';
    } else {
        moreBtn.style.display = 'block';
    }

    console.log(commentsToShow)
}


const showMoreComments = (postid) => {
    let commentsToShowElement = document.getElementById(`commentsShowing-${postid}`)
    commentsToShow = Number(commentsToShowElement.value);
    commentsToShowElement.value = commentsToShow + 3
    updateItemsVisbility(postid, commentsToShow + 3);
}


const showLessComments = (postid) => {
    let commentsToShowElement = document.getElementById(`commentsShowing-${postid}`)
    commentsToShow = Number(commentsToShowElement.value);
    commentsToShowElement.value = commentsToShow - 3
    updateItemsVisbility(postid, commentsToShow - 3);
}
