import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
        except:
            print("Ошибка: Соединение с сервером потеряно.")
            client_socket.close()
            break


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))

    # Получаем приветствие от сервера
    response = client.recv(1024).decode()
    if response != "HELLO":
        print("Ошибка: неверное приветствие от сервера")
        client.close()
        return

    # Отправляем подтверждение серверу
    client.send("HELLO-APPROVE".encode())

    # Запрашиваем и отправляем имя пользователя
    username = input("Введите ваше имя: ")
    # client.send(username.encode())

    # Запускаем поток для приема сообщений от сервера
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    # Отправляем сообщения серверу
    while True:
        message = input()
        client.send(f"{username}: {message}".encode())


if __name__ == "__main__":
    main()
