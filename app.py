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
