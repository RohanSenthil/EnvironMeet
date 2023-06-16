const sharePost = (postid) => {

    fetch(`/post/share/${postid}`, {method:'POST'}).then((res) => res.json()).then((data) => {
        if (data['success']) {

            const nativeLinkElem = document.getElementById(`nativeLink_${ postid }`);
            nativeLinkElem.value = encodeURIComponent(data['native'])

            const default_text = encodeURIComponent('Check%20out%20this%20post%20on%20EnvironMeet%3A%0A');

            const teleLinkElem = document.getElementById(`teleLink_${ postid }`);
            const waLinkElem = document.getElementById(`waLink_${ postid }`);
            const twitterLinkElem = document.getElementById(`twitterLink_${ postid }`);
            const redditLinkElem = document.getElementById(`redditLink_${ postid }`);
            const fbLinkElem = document.getElementById(`fbLink_${ postid }`);

            let teleLink = encodeURIComponent(`https://t.me/share/url?url=${data['native']}&text=${default_text}`);
            let waLink = encodeURIComponent(`https://api.whatsapp.com/send?text=${default_text}%20${data['native']}`);
            let twitterLink = encodeURIComponent(`https://twitter.com/intent/tweet?url=${data['native']}&text=${default_text}`);
            let redditLink = encodeURIComponent(`https://reddit.com/submit?url=${data['native']}&title=${default_text}`);
            let fbLink = encodeURIComponent(`https://www.facebook.com/sharer.php?u=${data['native']}`);

            teleLinkElem.setAttribute('href', teleLink);
            waLinkElem.setAttribute('href', waLink);
            twitterLinkElem.setAttribute('href', twitterLink);
            redditLinkElem.setAttribute('href', redditLink);
            fbLinkElem.setAttribute('href', fbLink);
        }
    })
    .catch((e) => alert('ERROR: Unable to generate links.'));

    const modal = document.getElementById(`sharePostModal_${postid}`);
    $(modal).modal('show');
}