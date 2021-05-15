import socket

import thread   # thread.py

server_address = ("127.0.0.1", 59420)
api_key = "04c2fe7409f870cddc889cad96d458c9"

print(10*"=" + "Server has started" + "="*10)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_p:
    sock_p.bind(server_address)
    sock_p.listen(1)

    # This bool, as the name suggests,
    # checks if maximum number of threads are running.
    # This only accounts for threads and not connections.
    hasLimitExceeded = False

    while True:
        if not hasLimitExceeded:
            sock_a, sockname = sock_p.accept()
            t = thread.Thread(sock_a, sockname, api_key)
            t.StartThread()

        # Only allow 3 threads at a time
        # 4 because it also counts this main thread
        if thread.threading.active_count() >= 4:
            hasLimitExceeded = True