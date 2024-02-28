import socket
import threading

# Список для хранения сокетов всех подключенных клиентов
clients = []


def handle_client(client_socket, client_address):
    # Приветствие клиента
    client_socket.send("HELLO".encode())

    # Проверяем подтверждение от клиента
    response = client_socket.recv(1024).decode()
    if response != "HELLO-APPROVE":
        print("Ошибка: клиент не подтвердил подключение")
        client_socket.close()
        return

    # Добавляем клиентский сокет в список клиентов
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                broadcast(f"{client_address[0]}:{client_address[1]}: {message}")
        except:
            print(f"Пользователь {client_address[0]}:{client_address[1]} отключился.")
            client_socket.close()
            # Удаляем клиентский сокет из списка клиентов при отключении
            clients.remove(client_socket)
            break


def broadcast(message):
    for client_socket in clients:
        client_socket.send(message.encode())


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen(5)

    print("Сервер запущен и ожидает подключений...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Подключение установлено с {client_address[0]}:{client_address[1]}")

        client_socket_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_socket_thread.start()


if __name__ == "__main__":
    main()
