
from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)

folder_path = r'C:\Users\admin\Downloads'

@app.route('/')
def index():
    try:
        files = os.listdir(folder_path)
    except FileNotFoundError:
        return "Папка не найдена", 404

    html_content = '''
    <html>
        <head><title>Логи контейнеров</title></head>
        <body>
            <h1>Доступные контейнеры: {{ folder }}</h1>
            <ul>
                {% for file in files %}
                    <li><a href="/files/{{ file }}">{{ file }}</a></li>
                {% endfor %}
            </ul>
        </body>
    </html>
    '''
    return render_template_string(html_content, folder=folder_path, files=files)

@app.route('/files/<filename>')
def serve_file(filename):
    try:
        return send_from_directory(folder_path, filename)
    except FileNotFoundError:
        return "Файл не найден", 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
