
const newPostInput = document.getElementById('newPostInput');
const charCounter = document.getElementById('charCounter');
const commentInput = document.getElementById('commentInput');

newPostInput.style.height = `height: ${newPostInput.scrollHeight}`;

const charLimit = (limitField, limitNum) => {

    if (limitField.value.length > limitNum) {
        limitField.value = limitField.value.substring(0, limitNum)
        charCounter.innerText = 0;
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

commentInput.addEventListener('input', (e) => {

    maxChars = 250;

    charLimit(e.target, maxChars);
})