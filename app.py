from flask import Flask, render_template, request, jsonify # pyright: ignore[reportMissingImports]
import sqlite3
import os
from models.object_detection import detect_objects
from utils.instruction_generator import generate_instruction

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize database
def init_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS preferences
                 (id INTEGER PRIMARY KEY, user_id TEXT, language TEXT, volume INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/navigation')
def navigation():
    return render_template('navigation.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    image_bytes = file.read()

    detections = detect_objects(image_bytes)
    instruction = generate_instruction(detections)

    return jsonify({
        'detections': detections,
        'instruction': instruction
    })

@app.route('/save_settings', methods=['POST'])
def save_settings():
    data = request.json
    user_id = data.get('user_id', 'default')
    language = data.get('language', 'en')
    volume = data.get('volume', 50)

    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO preferences (user_id, language, volume) VALUES (?, ?, ?)',
              (user_id, language, volume))
    conn.commit()
    conn.close()

    return jsonify({'status': 'saved'})

@app.route('/get_settings')
def get_settings():
    user_id = request.args.get('user_id', 'default')
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('SELECT language, volume FROM preferences WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return jsonify({'language': row[0], 'volume': row[1]})
    return jsonify({'language': 'en', 'volume': 50})

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000))) 