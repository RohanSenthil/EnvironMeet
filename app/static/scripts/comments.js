const addComment = (postid) => {
    let searchData = new URLSearchParams();
    searchData.append('desc', document.getElementById(`commentInput-${postid}`).value);
    console.log(document.getElementById(`commentInput-${postid}`).value)

    fetch(`/post/comment/add/${postid}`, {method: 'POST', 
    body: searchData}).then((res) => res.json())
    .then((data) => { console.log(data)
        if (data['success']) {
            const commentDiv = document.getElementById(`form-reload-${data['postid']}`);

            $(commentDiv).load(document.URL + ' ' + `#form-reload-${data['postid']}`);
        }

    })
    .catch((e) => alert(e, 'ERROR: This comment cannot be posted'));

    return false;
}