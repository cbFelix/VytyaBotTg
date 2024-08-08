function handleResponse(response) {
    if (!response.ok) {
        return response.json().then(error => {
            throw new Error(error.error || 'Unknown error');
        });
    }
    return response.json();
}

function updateBotStatus() {
    fetch('/bot/status/')
        .then(handleResponse)
        .then(data => {
            document.getElementById('bot-status').innerText = data.status;
        })
        .catch(error => {
            alert('Failed to fetch bot status: ' + error.message);
        });
}

function startBot() {
    fetch('/bot/start-bot/')
        .then(handleResponse)
        .then(data => {
            updateBotStatus();
        })
        .catch(error => {
            alert('Failed to start bot: ' + error.message);
        });
}

function stopBot() {
    fetch('/bot/stop-bot/')
        .then(handleResponse)
        .then(data => {
            updateBotStatus();
        })
        .catch(error => {
            alert('Failed to stop bot: ' + error.message);
        });
}

function restartBot() {
    fetch('/bot/restart-bot/')
        .then(handleResponse)
        .then(data => {
            updateBotStatus();
        })
        .catch(error => {
            alert('Failed to restart bot: ' + error.message);
        });
}
