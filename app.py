import os
import shutil
import tempfile

from flask import send_file, send_from_directory
from flask import Flask, render_template,  current_app
from werkzeug.security import safe_join

# здесь указать папку относительное app.py
BASE_DIR = "images/image" 
app = Flask(__name__)

@app.route('/')
def index():
    items = list_directory(BASE_DIR)
    return render_template('index.html', items=items)


@app.route('/explore/<path:subpath>')
def explore(subpath):
    folder_path = safe_join(subpath)
    items = list_directory(folder_path)
    return render_template('index.html', items=items)


@app.route('/download-file/<path:path>')
def download_file(path):
    """Здесь получаем полный путь, а потом делим"""
    partial = path.split('/')
    filename = partial[-1]
    partial.pop()
    directory = '/'.join(partial)
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/download_folder/<path:path>')
def download_folder(path):
    folder_name = os.path.basename(path) 
    # Создаем временный файл для хранения архива
    temp_file = tempfile.mktemp()
    # Архивируем папку
    shutil.make_archive(temp_file, 'zip', path)
    # Отправляем архив пользователю
    response = send_file(temp_file + '.zip', download_name = f"{folder_name}.zip", as_attachment=True)
    # Удаляем временный файл после отправки
    os.remove(temp_file + '.zip')

    return response



def list_directory(directory):
    """теперь объект item имеет еще поле path. 
    Если не передавать полный path в index.html,
    то при переходе назад по кнопке в браузере папка не будет найдена
    """
    result = []
    for item in sorted(os.listdir(directory)):
        item_path = safe_join(directory, item)
        item_type = 'dir' if os.path.isdir(item_path) else 'file'
        result.append({'path': item_path, 'name':item, 'type': item_type})
    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
