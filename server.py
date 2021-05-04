import socket
import threading
import os
import json

import thread

from urllib.error import HTTPError
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlparse, urlunparse


server_address = ("127.0.0.1", 59420)
api_key = "04c2fe7409f870cddc889cad96d458c9"

print(10*"=" + "Server has started" + "="*10)




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_p:
    sock_p.bind(server_address)
    sock_p.listen(2)

    numOfThreads = 0

    while True:
        if numOfThreads > 2:
            continue

        sock_a, sockname = sock_p.accept()
        t = thread.Thread(sock_a, sockname, api_key)
        t.StartThread()