let socketio = io();
      
const messages = document.getElementById("messages");

const createMessage = (data) => {

    let content = document.createElement('div');
    content.classList.add(data.sysgen ? 'text': 'message');

    let timestampElement = document.createElement('span');
    timestampElement.classList.add('muted');
    timestampElement.textContent = data.timestamp || new Date().toLocaleString('en-GB');

    if (data.sysgen) {

        let textContentElement = document.createElement('span');
        textContentElement.classList.add('text-content');
        textContentElement.textContent = `${data.name} ${data.message}`;
        
        content.appendChild(textContentElement);
        content.appendChild(timestampElement)
    } 
    else {

        if (current_user == data.name) {
            content.classList.add('my-msg')
        }

        let textRow = document.createElement('div');
        textRow.classList.add('text-row');

        let nameElement = document.createElement('span');
        let strongElement = document.createElement('strong');
        strongElement.textContent = data.name;
        
        nameElement.appendChild(strongElement)
        textRow.appendChild(nameElement);
        textRow.appendChild(timestampElement);
        content.appendChild(textRow);

        let textRowMsg = document.createElement('div');
        textRowMsg.classList.add('text-row', 'theMsg');
        textRowMsg.textContent = data.message;
        content.appendChild(textRowMsg);
    }

    messages.appendChild(content);

};

socketio.on("message", (data) => {
    createMessage(data);
});

const sendMessage = () => {
    const message = document.getElementById("message");
    if (message.value == "") return;
    socketio.emit("message", { data: message.value });
    message.value = "";
};

const sendBtn = document.getElementById('send-btn');

sendBtn.addEventListener('click', () => {
    sendMessage()
})