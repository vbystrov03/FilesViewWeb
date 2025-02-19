from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)

base_folder_path = '/mnt/logs'

def is_directory(path):
    return os.path.isdir(path)

# Главная страница
@app.route('/')
def index():
    try:
        files = os.listdir(base_folder_path)
        files_info = [{'name': file, 'is_directory': is_directory(os.path.join(base_folder_path, file))} for file in files]
    except FileNotFoundError:
        return "Папка не найдена", 404

    html_content = '''
    <html>
        <head><title>Логирование контейнеров</title></head>
        <body>
            <h1>Доступные контейнеры</h1>
            <ul>
                {% for file in files %}
                    <li>
                        {% if file.is_directory %}
                            <a href="/folder/{{ file.name }}">{{ file.name }}</a>
                        {% else %}
                            {{ file.name }}
                        {% endif %}
                    </li>
                {% endfor %}
            </ul>
        </body>
    </html>
    '''
    return render_template_string(html_content, files=files_info)

@app.route('/folder/<path:folder_path>')
def show_folder(folder_path):
    full_path = os.path.join(base_folder_path, folder_path)

    try:
        files = os.listdir(full_path)
        files_info = [{'name': file, 'is_directory': is_directory(os.path.join(full_path, file))} for file in files]
    except FileNotFoundError:
        return "Папка не найдена", 404

    html_content = '''
    <html>
        <head><title>Содержимое контейнера: {{ folder }}</title></head>
        <body>
            <h1>Содержимое контейнера: {{ folder }}</h1>
            <ul>
                <li><a href="/">Назад</a></li>
                {% for file in files %}
                    <li>
                        {% if file.is_directory %}
                            <a href="/folder/{{ folder }}/{{ file.name }}">{{ file.name }}</a>
                        {% else %}
                            <a href="/folder/{{ folder }}/files/{{ file.name }}">{{ file.name }}</a>
                        {% endif %}
                    </li>
                {% endfor %}
            </ul>
        </body>
    </html>
    '''
    return render_template_string(html_content, folder=folder_path, files=files_info)

@app.route('/folder/<path:folder_path>/files/<filename>')
def serve_file(folder_path, filename):
    try:
        full_path = os.path.join(base_folder_path, folder_path, filename)
        return send_from_directory(os.path.join(base_folder_path, folder_path), filename)
    
    except FileNotFoundError:
        return "Файл не найден", 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
