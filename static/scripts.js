function scrollToBottom() {
    var chatHistory = document.getElementById('chat_history');
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function animateBotMessage(element) {
    const message = element.innerText;
    element.innerText = '';
    const words = message.split(' ');

    let index = 0;
    const interval = setInterval(() => {
        if (index < words.length) {
            element.innerHTML += words[index] + ' ';
            index++;
        } else {
            clearInterval(interval);
        }
    }, 150); // Adjust the speed here (300ms per word
}

window.onload = function() {
    scrollToBottom();
    const botMessages = document.querySelectorAll('.bot-message');
    if (botMessages.length > 0) {
        animateBotMessage(botMessages[botMessages.length - 1]); // Animate only the last bot message
    }
};


