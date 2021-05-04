# Send/Receive message length before Sending/Receiving the actual message
def SendMessage(message, sock):
    message = message.encode(encoding='utf-8')
    messageLength = len(message).to_bytes(4, byteorder='big')
    sock.send(messageLength)
    sock.send(message)

def ReceiveMessage(sock):
    messageLength = sock.recv(4)
    messageLength = int.from_bytes(messageLength, byteorder='big')
    return sock.recv(messageLength).decode(encoding='utf-8')