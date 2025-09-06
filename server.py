from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Хранилище пикселей
pixels = {}
pending_commands = []

# Главная страница с интерфейсом
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Статические файлы (CSS, JS)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API для получения состояния
@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(pixels)

# API для отправки команды
@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.json
    x = data.get('x')
    y = data.get('y')
    color = data.get('color')
    
    if all([x is not None, y is not None, color]):
        key = f"{x}_{y}"
        pixels[key] = color
        
        command = f"{x} {y} {color}"
        pending_commands.append(command)
        
        return jsonify({'status': 'success'})
    
    return jsonify({'status': 'error'})

# API для ESP32 - получение команд
@app.route('/api/commands', methods=['GET'])
def get_commands():
    if pending_commands:
        command = pending_commands.pop(0)
        return jsonify({'command': command})
    return jsonify({'command': None})

# Сброс поля
@app.route('/api/reset', methods=['POST'])
def reset_pixels():
    global pixels, pending_commands
    pixels = {}
    pending_commands = []
    return jsonify({'status': 'reset'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
