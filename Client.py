import socket
import json

# Загрузка конфигурации
with open('config.json', 'r') as f:
    config = json.load(f)

HOST = config['server']['host']
PORT = config['server']['port']
BUFFER_SIZE = config['client']['buffer_size']

# Функция для получения списка команд с сервера
def get_commands():
    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send('commands'.encode())
    commands = sock.recv(BUFFER_SIZE).decode()
    sock.close()
    return commands

while True:
    try:

        print('\n''\n''\n'"Список доступных команд:")
        print('ls - Просмотр содержимого текущей директории', '\n'
              'pwd - Получение текущего пути','\n'
              'mkdir <directory_name> - Создание папки','\n'
              'rmdir <directory_name> - Удаление папки','\n'
              'rm <file_name> - Удаление файла','\n'
              'mv <source_file> <destination_file> - Переименование файла','\n'
              'put <file_name> <data> - Копирование файла на сервер','\n'
              'get <file_name> - Копирование файла с сервера','\n'
              'exit - Завершение работы программы')

        sock = socket.socket()
        sock.connect((HOST, PORT))

        request = input('Выберите команду: ')
        print(f'Отправлена команда: {request}')

        sock.send(request.encode())

        response = sock.recv(BUFFER_SIZE).decode()
        print(f'Получен результат: {response}')

    except KeyboardInterrupt:
        print("\nКлиент остановлен.")
        break

    finally:
        sock.close()
