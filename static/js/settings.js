// Settings page JavaScript

const settingsForm = document.getElementById('settings-form');
const languageSelect = document.getElementById('language');
const volumeInput = document.getElementById('volume');

// Load settings on page load
window.addEventListener('load', loadSettings);

settingsForm.addEventListener('submit', saveSettings);

async function loadSettings() {
    try {
        const response = await fetch('/get_settings');
        const data = await response.json();
        languageSelect.value = data.language;
        volumeInput.value = data.volume;
    } catch (err) {
        console.error('Error loading settings:', err);
    }
}

async function saveSettings(e) {
    e.preventDefault();
    const formData = new FormData(settingsForm);
    const data = {
        user_id: 'default', // For simplicity
        language: formData.get('language'),
        volume: parseInt(formData.get('volume'))
    };

    try {
        const response = await fetch('/save_settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        localStorage.setItem("language", data.language);
        localStorage.setItem("volume", data.volume);
        alert('Settings saved!');
    } catch (err) {
        console.error('Error saving settings:', err);
        alert('Error saving settings.');
    }
}