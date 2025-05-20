from flask import Flask, render_template, request
import time
import threading

app = Flask(__name__)

# Функции для работы с файлами
def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except:
        return '0'

def write_file(filename, value):
    with open(filename, 'w') as f:
        f.write(str(value))

# Функция для автоматического управления светом
def auto_light_control():
    while True:
        if read_file('nutrition.txt') == '1':  # Если питание включено
            light_level = int(read_file('light.txt'))
            if light_level < 50:
                # Включаем белый свет (все цвета)
                write_file('red.txt', '1')
                write_file('green.txt', '1')
                write_file('blue.txt', '1')
            else:
                # Проверяем, не были ли цвета включены вручную
                if not (read_file('buttonR.txt') == '1' or 
                        read_file('buttonG.txt') == '1' or 
                        read_file('buttonB.txt') == '1'):
                    write_file('red.txt', '0')
                    write_file('green.txt', '0')
                    write_file('blue.txt', '0')
        time.sleep(1)

# Запускаем поток для автоматического управления
thread = threading.Thread(target=auto_light_control)
thread.daemon = True
thread.start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Обработка кнопки питания
        if 'nutrition' in request.form:
            current = read_file('nutrition.txt')
            new_value = '0' if current == '1' else '1'
            write_file('nutrition.txt', new_value)
        
        # Обработка цветовых кнопок
        for color in ['R', 'G', 'B']:
            if color in request.form:
                current = read_file(f'button{color}.txt')
                new_value = '0' if current == '1' else '1'
                write_file(f'button{color}.txt', new_value)
                # Если питание включено, меняем состояние цвета
                if read_file('nutrition.txt') == '1':
                    write_file(f'{color.lower()}.txt', new_value)

# Чтение текущих состояний
    nutrition = read_file('nutrition.txt')
    light_level = read_file('light.txt')
    colors = {
        'red': read_file('red.txt'),
        'green': read_file('green.txt'),
        'blue': read_file('blue.txt')
    }
    buttons = {
        'R': read_file('buttonR.txt'),
        'G': read_file('buttonG.txt'),
        'B': read_file('buttonB.txt')
    }
    
    return render_template('index.html', 
                         nutrition=nutrition,
                         light_level=light_level,
                         colors=colors,
                         buttons=buttons)

if __name__ == '__main__':
    # Инициализация файлов, если они не существуют
    for file in ['light.txt', 'buttonR.txt', 'buttonG.txt', 'buttonB.txt', 
                 'nutrition.txt', 'red.txt', 'green.txt', 'blue.txt']:
        try:
            open(file, 'r').close()
        except:
            write_file(file, '0')
    
    app.run(host='0.0.0.0', port=8080)
