import socket
from select import select

tasks = []

to_read = {}
to_write = {}


def server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(('localhost', 5001))
	server_socket.listen()

	while True:
		print('server before')
		yield ('read', server_socket)
		print('server after')

		client_socket, addr = server_socket.accept()
		print('Connection from', addr)
		client(client_socket)
		tasks.append(client(client_socket))


def client(client_socket):
	while True:
		print('before first')
		yield ('read', client_socket)
		print('after first')
		request = client_socket.recv(4096)
		if not request:
			break
		else:
			response = 'Hello world\n'.encode()
			print('before second')
			yield ('write', client_socket)
			print('after second')
			client_socket.send(response)
	client_socket.close()


def event_loop():
	
	while any([tasks, to_read, to_write]):
		while not tasks:
			ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

			for sock in ready_to_read:
				tasks.append(to_read.pop(sock))
			for sock in ready_to_write:
				tasks.append(to_write.pop(sock))
		try:
			task = tasks.pop(0)
			reason, sock = next(task)
			if reason == 'read':
				to_read[sock] = task
			if reason == 'write':
				to_write[sock] = task
		except StopIteration:
			print("All done")


tasks.append(server())
event_loop()
