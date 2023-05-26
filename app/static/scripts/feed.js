
const newPostInput = document.getElementById('newPostInput');
newPostInput.style.height = `height: ${newPostInput.scrollHeight}`

const charCounter = document.getElementById('charCounter');

const charLimit = (limitField, limitNum) => {

    if (limitField.value.length > limitNum) {
        limitField.value = limitField.value.substring(0, limitNum)
        charCounter.innerText = 0
    }
}

newPostInput.addEventListener('input', (e) => {
    e.target.style.height = "auto";
    e.target.style.height = `${e.target.scrollHeight}px`;

    maxChars = 200

    if (Number(charCounter.innerText) >= 0) {
        charCounter.innerText = maxChars - newPostInput.value.length
    }

    charLimit(e.target, maxChars)
})
