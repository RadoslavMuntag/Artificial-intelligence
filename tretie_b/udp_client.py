import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server IP address and port
server_address = ('172.30.207.170', 6789)

# Message to send
message = b'This is a test message'

try:
    # Send message to the server
    print(f'Sending: {message}')
    sent = sock.sendto(message, server_address)

finally:
    # Close the socket
    print('Closing socket')
    sock.close()
