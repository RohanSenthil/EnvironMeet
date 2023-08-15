
const newPostInput = document.getElementById('newPostInput');
const charCounter = document.getElementById('charCounter');
const commentInputs = document.getElementsByClassName('commentInput');
const addImageForPost = document.getElementById('addImageForPost');
const previewImageHolder = document.getElementById('previewImage');
const editPostInputs = document.getElementsByClassName('editPostInput');
const charCounters = document.getElementsByClassName('charCounters');
const editPostBtns = document.getElementsByClassName('editPostBtn');
const newPostBtn = document.getElementById('newPostBtn');
const tabBtns = document.getElementsByClassName('tab-btn');
const tabGroups = document.getElementsByClassName('tab-group');

if (newPostInput) {
    newPostInput.style.height = `height: ${newPostInput.scrollHeight}`;
}

const charLimit = (limitField, limitNum, counter=null) => {
    if (limitField.value.length > limitNum) {
        limitField.value = limitField.value.substring(0, limitNum)
        if (counter) {
            counter.textContent = 0;
        }
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

if (newPostInput) {
    newPostInput.addEventListener('input', (e) => {
        e.target.style.height = "auto";
        e.target.style.height = `${e.target.scrollHeight}px`;

        if (newPostInput.value.length > 0) {
            newPostInput.classList.remove('error-border');
        }

        maxChars = 500;

        if (Number(charCounter.textContent) >= 0) {
            charCounter.textContent = maxChars - newPostInput.value.length;
        }

        charLimit(e.target, maxChars, charCounter);
    })
}

for (let i = 0; i < commentInputs.length; i++) {
    commentInputs[i].addEventListener('input', (e) => {

        maxChars = 250;
        charLimit(e.target, maxChars);
    })
}

if (addImageForPost) {
    addImageForPost.addEventListener('input', (e) => {
        previewImage(e.target, previewImageHolder)
    })
}

for (let i = 0; i < editPostInputs.length; i++) {
    editPostInputs[i].style.height = `height: ${editPostInputs[i].scrollHeight}`;

    editPostInputs[i].addEventListener('input', (e) => {
        e.target.style.height = "auto";
        e.target.style.height = `${e.target.scrollHeight}px`;
        
        if (editPostInputs[i].value.length > 0) {
            editPostInputs[i].classList.remove('error-border');
        }

        maxChars = 500;

        if (Number(charCounters[i].textContent) >= 0) {
            charCounters[i].textContent= maxChars - editPostInputs[i].value.length;
        }

        charLimit(e.target, maxChars, charCounters[i]);
    })
}

for (let i = 0; i < editPostBtns.length; i++) {

    editPostBtns[i].addEventListener('click', (e) => {

        if (editPostInputs[i].value.length <= 0 || editPostInputs[i].value.length > 500) {
            e.preventDefault()
            e.stopPropagation()

            editPostInputs[i].classList.add('error-border');
        } else {
            editPostInputs[i].classList.remove('error-border');
        }

    })
}

if (newPostBtn) {
    newPostBtn.addEventListener('click', (e) => {
        if (newPostInput.value.length <= 0 || newPostInput.value.length > 500) {
            e.preventDefault()
            e.stopPropagation()
    
            newPostInput.classList.add('error-border');
        } else {
            newPostInput.classList.remove('error-border');
        }
    })
}

for (let i = 0; i < tabBtns.length; i++) {
    tabBtns[i].addEventListener('click', (e) => {
        for (let i = 0; i < tabBtns.length; i++) {
            tabBtns[i].classList.remove('active');
        }
        for (let i = 0; i < tabGroups.length; i++) {
            tabGroups[i].style.display = 'none';
        }
        e.target.classList.add('active');
        
        let tabName = (e.target.id).split('-')[0] + '-' + (e.target.id).split('-')[1]
        if (document.getElementById(tabName)) {
            document.getElementById(tabName).style.display = 'block';
        }

    })
}
    // Function to reset the inactivity timer
    function resetInactivityTimer() {
        fetch('/reset_activity', { method: 'POST' }); // Send a request to the server to reset the last_activity
    }

    // Add event listeners to reset the timer on user interaction
    document.addEventListener('click', resetInactivityTimer);
    document.addEventListener('keydown', resetInactivityTimer);

    // Call the resetInactivityTimer function on page load to start the timer
    resetInactivityTimer();