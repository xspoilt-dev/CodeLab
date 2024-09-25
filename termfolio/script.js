const output = document.getElementById('output');
const inputField = document.getElementById('input');
const inputText = document.getElementById('input-text');


setTimeout(() => {
    document.querySelector('.terminal-container').style.display = 'flex';
}, 4000);

const commands = {
    'help': 'Available commands: help, whoami, skills, clear',
    'whoami': 'Name: Minhajul Islam\nWork : Software Developer\nFacebook: https://www.fb.me/xspoilt\nTelegram: https://www.t.me/x_spoilt',
    'skills': 'Python, JavaScript, PHP, MySQL',
    'clear': '',
    'cls': ''
};

function executeCommand(command) {
    const cmd = command.trim().toLowerCase();
    if (commands[cmd]) {
        return commands[cmd];
    } else {
        return `'${cmd}' is not a recognized command. Type 'help' for available commands.`;
    }
}

function appendOutput(text) {
    const div = document.createElement('div');
    div.textContent = text;
    output.appendChild(div);
}

inputField.addEventListener('input', function(event) {
    inputText.textContent = inputField.value;
});

inputField.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        const command = inputField.value;
        appendOutput(`xspoilt@cmd:~$ ${command}`);
        const response = executeCommand(command);
        if (command === 'clear') {
            output.innerHTML = '';
        } else {
            appendOutput(response);
        }
        inputField.value = '';
        inputText.textContent = '';
    }
});
