// Navigation page JavaScript

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const instructionEl = document.getElementById('instruction');
const startBtn = document.getElementById('start-btn');

let stream;
let intervalId;

startBtn.addEventListener('click', startDetection);

async function startDetection() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        startBtn.disabled = true;
        startBtn.textContent = 'Detecting...';

        // Start capturing frames every 1 second
        intervalId = setInterval(captureAndDetect, 1000);
    } catch (err) {
        console.error('Error accessing webcam:', err);
        instructionEl.textContent = 'Error: Cannot access webcam.';
    }
}

function captureAndDetect() {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);

    canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('image', blob, 'frame.jpg');

        try {
            const response = await fetch('/detect', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            // Display detections on canvas
            drawDetections(data.detections);

            // Update instruction
            instructionEl.textContent = data.instruction;

            // Speak instruction
            speak(data.instruction);
        } catch (err) {
            console.error('Error detecting objects:', err);
        }
    });
}

function drawDetections(detections) {
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(video, 0, 0);

    detections.forEach(det => {
        const [x1, y1, x2, y2] = det.bbox;
        context.strokeStyle = '#ff0000';
        context.lineWidth = 2;
        context.strokeRect(x1, y1, x2 - x1, y2 - y1);

        context.fillStyle = '#ff0000';
        context.font = '16px Arial';
        context.fillText(`${det.class} ${det.confidence.toFixed(2)}`, x1, y1 - 5);
    });
}

function speak(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
    }
}

// Stop detection when leaving page
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    if (intervalId) {
        clearInterval(intervalId);
    }
});