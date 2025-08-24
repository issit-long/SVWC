// ... (previous JavaScript code remains the same until the event listeners)

// Update the event listeners to make API calls:

powerOnBtn.addEventListener('click', function() {
    fetch('/api/power', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            display: selectedDisplay,
            power_on: true
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Power on response:', data);
        simulatePowerOn();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to control power');
    });
});

// Similarly update all other control functions to use fetch API

// Add function to periodically update status
function updateStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            console.log('Status:', data);
            // Update UI with real status data
            for (let i = 1; i <= 4; i++) {
                const display = data[`display_${i}`];
                if (display) {
                    const indicator = document.querySelector(`#tv${i} .power-indicator`);
                    const content = document.querySelector(`#tv${i} .tv-content`);
                    const inputSpan = document.querySelector(`#tv${i} .tv-status span`);
                    
                    if (indicator) {
                        indicator.classList.toggle('on', display.power === 'on');
                    }
                    if (content) {
                        content.textContent = display.power === 'on' ? 
                            `Display ${i} - ${display.input.toUpperCase()}` : 
                            'No Signal';
                    }
                    if (inputSpan) {
                        inputSpan.textContent = display.input.toUpperCase();
                    }
                }
            }
        })
        .catch(error => {
            console.error('Error fetching status:', error);
        });
}

// Update status every 10 seconds
setInterval(updateStatus, 10000);
updateStatus(); // Initial update