const sharePost = (postid) => {

    const csrfTokenElem = document.getElementById(`sharePost${ postid }`).querySelector('input[name="csrf_token"]');
    
    if (csrfTokenElem) {
        csrfToken = csrfTokenElem.value
    } 
    else {
        csrfToken = null
    }


    fetch(`/post/share/${postid}`, {method:'POST', headers: {'X-CSRFToken': csrfToken},}).then((res) => res.json()).then((data) => {
        if (data['success']) {

            const url = encodeURI(data['native']);
            const default_text = encodeURIComponent('Check out this post on EnvironMeet:\n');

            const nativeLinkElem = document.getElementById(`nativeLink_${ postid }`);
            nativeLinkElem.textContent = url;

            const teleLinkElem = document.getElementById(`teleLink_${ postid }`);
            const waLinkElem = document.getElementById(`waLink_${ postid }`);
            const twitterLinkElem = document.getElementById(`twitterLink_${ postid }`);
            const redditLinkElem = document.getElementById(`redditLink_${ postid }`);
            const fbLinkElem = document.getElementById(`fbLink_${ postid }`);

            let teleLink = encodeURI(`https://t.me/share/url?url=${url}&text=${default_text}`);
            let waLink = encodeURI(`https://api.whatsapp.com/send?text=${default_text}%20${url}`);
            let twitterLink = encodeURI(`https://twitter.com/intent/tweet?url=${url}&text=${default_text}`);
            let redditLink = encodeURI(`https://reddit.com/submit?url=${url}&title=${default_text}`);
            let fbLink = encodeURI(`https://www.facebook.com/sharer.php?u=${url}`);

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