const sharePost = (postid) => {

    fetch(`/post/share/${postid}`, {method:'POST'}).then((res) => res.json()).then((data) => {
        if (data['success']) {
            const nativeLinkElem = document.getElementById(`nativeLink_${ postid }`);
            nativeLinkElem.value= data['native']

            const default_text = 'Check%20out%20this%20post%20on%20EnvironMeet%3A%0A';

            const teleLinkElem = document.getElementById(`teleLink_${ postid }`);
            const waLinkElem = document.getElementById(`waLink_${ postid }`);
            const twitterLinkElem = document.getElementById(`twitterLink_${ postid }`);
            const redditLinkElem = document.getElementById(`redditLink_${ postid }`);
            const fbLinkElem = document.getElementById(`fbLink_${ postid }`);

            teleLinkElem.href = `https://t.me/share/url?url=${data['native']}&text=${default_text}`;
            waLinkElem.href = `https://api.whatsapp.com/send?text=${default_text}%20${data['native']}`;
            twitterLinkElem.href = `https://twitter.com/intent/tweet?url=${data['native']}&text=${default_text}`;
            redditLinkElem.href = `https://reddit.com/submit?url=${data['native']}&title=${default_text}`;
            fbLinkElem.href = `https://www.facebook.com/sharer.php?u=${data['native']}`;
        }
    })
    .catch((e) => alert(e));

    const modal = document.getElementById(`sharePostModal_${postid}`);
    $(modal).modal('show');
}