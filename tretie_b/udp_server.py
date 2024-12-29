import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address and port
server_address = ('0.0.0.0', 6789)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

while True:
    print('Waiting to receive message...')
    data, address = sock.recvfrom(4096)

    print(f'Received {len(data)} bytes from {address}')
    print(data)

    if data:
        print('Sending response back to client')
        sock.sendto(b'Message received', address)
