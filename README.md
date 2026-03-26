# Blind Navigation AI

A modern web application that helps visually impaired users navigate safely using AI-powered obstacle detection and real-time audio instructions.

## Features

- Real-time object detection using YOLOv8
- Audio navigation instructions
- Modern glassmorphism UI design
- Dark/light mode toggle
- User preferences storage
- Responsive design

## Installation

1. Clone or download the project files.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Open your browser and go to `http://localhost:5000`

## Project Structure

```
blind-navigation-ai/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── index.html
│   ├── navigation.html
│   ├── settings.html
│   └── about.html
├── static/                # Static files
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── script.js
│   │   ├── navigation.js
│   │   └── settings.js
│   └── images/            # Logo and favicon
├── models/                # AI models
│   └── object_detection.py
└── utils/                 # Utility functions
    └── instruction_generator.py
```

## Usage

1. On the home page, click "Start Navigation".
2. Allow webcam access when prompted.
3. Click "Start Detection" to begin real-time obstacle detection.
4. Listen to audio instructions and follow them to navigate safely.

## Technologies Used

- Backend: Python Flask
- AI: YOLOv8 (Ultralytics)
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- TTS: Web Speech API

## Note

The YOLOv8 model will be downloaded automatically on first run. Ensure you have a stable internet connection.