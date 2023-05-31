
const newPostInput = document.getElementById('newPostInput');
const charCounter = document.getElementById('charCounter');
const commentInputs = document.getElementsByClassName('commentInput');
const addImageForPost = document.getElementById('addImageForPost');
const previewImageHolder = document.getElementById('previewImage');

newPostInput.style.height = `height: ${newPostInput.scrollHeight}`;

const charLimit = (limitField, limitNum) => {

    if (limitField.value.length > limitNum) {
        limitField.value = limitField.value.substring(0, limitNum)
        charCounter.innerText = 0;
    }
}

const removePreview = (target) => {
    while (target.hasChildNodes()) {
        target.removeChild(target.firstChild);
    }
}

const previewImage = (src, target) => {

    // Reset
    removePreview(target)

    // Preview
    file = src.files[0]

    if (file) {
        const fileRead = new FileReader();
        fileRead.readAsDataURL(file);
        fileRead.addEventListener('load', () => {
            let img = document.createElement('img');
            let closeIcon = document.createElement('span');
            let btn = document.createElement('button');

            img.src = fileRead.result;

            closeIcon.classList.add('closeIcon');

            btn.setAttribute('type', 'button');
            btn.addEventListener('click', () => {
                removePreview(previewImageHolder)
            });
            btn.appendChild(closeIcon)

            img.src = fileRead.result;

            target.appendChild(img);
            target.appendChild(btn);
        })
    }
    
}

newPostInput.addEventListener('input', (e) => {
    e.target.style.height = "auto";
    e.target.style.height = `${e.target.scrollHeight}px`;

    maxChars = 500;

    if (Number(charCounter.innerText) >= 0) {
        charCounter.innerText = maxChars - newPostInput.value.length;
    }

    charLimit(e.target, maxChars);
})

for (let i = 0; i < commentInputs.length; i++) {
    commentInputs[i].addEventListener('input', (e) => {

        maxChars = 250;

        charLimit(e.target, maxChars);
    })
}

addImageForPost.addEventListener('input', (e) => {
    previewImage(e.target, previewImageHolder)
})