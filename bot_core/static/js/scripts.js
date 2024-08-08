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

document.getElementById('bot-config-form').addEventListener('submit', function(event) {

    const token = document.getElementById('token').value;
    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    fetch('/bot/update-token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ token: token })
    })
    .then(handleResponse)
    .then(data => {
        alert('Token updated successfully');
        updateBotStatus();
    })
    .catch(error => {
        alert('Failed to update token: ' + error.message);
    });
});
