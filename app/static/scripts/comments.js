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