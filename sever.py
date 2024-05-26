import socket
import json
import os
import shutil

def process(request):
    command, *args = request.split()

    if command == 'ls':
        return '; '.join(os.listdir())

    elif command == 'pwd':
        return os.getcwd()

    elif command == 'mkdir':
        if args:
            dirname = args[0]
            os.mkdir(dirname)
            return f'Папка {dirname} создана'
        else:
            return 'Не указано имя папки для создания'

    elif command == 'rmdir':
        if args:
            dirname = args[0]
            shutil.rmtree(dirname)
            return f'Папка {dirname} удалена'
        else:
            return 'Не указано имя папки для удаления'

    elif command == 'rm':
        if args:
            filename = args[0]
            os.remove(filename)
            return f'Файл {filename} удален'
        else:
            return 'Не указано имя файла для удаления'

    elif command == 'mv':
        if len(args) == 2:
            src, dst = args
            os.rename(src, dst)
            return f'Файл {src} переименован в {dst}'
        else:
            return 'Неправильное количество аргументов для переименования файла'

    elif command == 'put':
        if len(args) == 2:
            filename, data = args
            with open(filename, 'w') as file:
                file.write(data)
            return f'Файл {filename} скопирован на сервер'
        else:
            return 'Неправильное количество аргументов для копирования файла на сервер'

    elif command == 'get':
        if args:
            filename = args[0]
            with open(filename, 'r') as file:
                data = file.read()
            return data
        else:
            return 'Не указано имя файла для копирования с сервера'

    else:
        return 'Неверная команда'

# Загрузка конфигурации
with open('config.json', 'r') as f:
    config = json.load(f)

HOST = config['server']['host']
PORT = config['server']['port']

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen()

print(f'Сервер запущен на порте {PORT}')

while True:
    conn, addr = sock.accept()
    print(f'Подключение клиента {addr}')

    request = conn.recv(config['client']['buffer_size']).decode()
    print(f'Получен запрос: {request}')

    response = process(request)

    conn.send(response.encode())

    conn.close()

sock.close()
