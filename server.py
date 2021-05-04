import socket
import threading
import os
import json

import myutils

from urllib.error import HTTPError
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlparse, urlunparse


server_address = ("127.0.0.1", 59420)
api_key = "04c2fe7409f870cddc889cad96d458c9"

print(10*"=" + "Server has started" + "="*10)

class MultiThread:
    sock = None
    address = None

    def __init__(self, s, add):
        self.sock = s
        self.address = add

    def GenerateThread(self):
        currentThread = threading.Thread(target=self.ThreadFunctionality)
        currentThread.start()

    def ThreadFunctionality(self):
        clientName = myutils.ReceiveMessage(self.sock)
        print(f"{clientName} has connected.")

        while True:
            airportCode = myutils.ReceiveMessage(self.sock)
            url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&limit=100&arr_icao={airportCode}"
            urlretrieve(url, f"./JSON/group_11_{clientName}.json")

            choice = myutils.ReceiveMessage(self.sock)

            if choice == "quit":
                print(f"{clientName} has disconnected")
                os.remove(f"./JSON/group_11_{clientName}.json")
                break
            
            with open(f"./JSON/group_11_{clientName}.json", 'r') as f:
                json_data = json.load(f)
            
            if choice == "arrived":
                msg = ""
                print(f"{clientName} has requested a list of all arrived flights.")

                for flight in json_data['data']:
                    if flight['flight_status'] == 'landed':
                        msg += 20*"-" + "\n"
                        msg += f"Flight IATA code:  {flight['flight']['iata'] } \n"
                        msg += f"Departure Airport: { flight['departure']['airport'] } \n"
                        msg += f"Arrival Time: { flight['arrival']['estimated'] } \n"
                        msg += f"Terminal: { flight['arrival']['terminal'] } \n"
                        msg += f"Gate: { flight['arrival']['gate'] } \n"
                msg += 20*"-" + "\n"

            elif choice == "delayed":
                msg = ""
                print(f"{clientName} has requested a list of all delayed flights.")

                for flight in json_data['data']:
                    if flight['departure']['delay'] != None and int(flight['departure']['delay']) > 0:
                        msg += 20*"-" + "\n"
                        msg += f"Flight IATA code: { flight['flight']['iata'] } \n"
                        msg += f"Departure Airport: { flight['departure']['airport'] } \n"
                        msg += f"Estimated Arrival Time: { flight['arrival']['estimated'] } \n"
                        msg += f"Terminal: { flight['arrival']['terminal'] } \n"
                        msg += f"Gate: { flight['arrival']['gate'] } \n"
                msg += 20*"-" + "\n"

            elif choice.startswith("city"):
                code = choice[5:]
                msg = ""
                print(f"{clientName} has requested a list of flights from {code}.")

                for flight in json_data['data']:
                    if flight['departure']['iata'] == code.upper():
                        msg += 20*"-" + "\n"
                        msg += f"Flight IATA code: { flight['flight']['iata'] }\n"
                        msg += f"Departure Airport: { flight['departure']['airport'] } \n"
                        msg += f"Departure Time: { flight['arrival']['estimated'] } \n"
                        msg += f"Estimated Arrival Time: { flight['arrival']['estimated'] } \n"
                        msg += f"Terminal: { flight['arrival']['terminal'] } \n"
                        msg += f"Gate: { flight['arrival']['gate'] } \n"
                msg += 20*"-" + "\n"

            elif choice.startswith("details"):
                code = choice[8:]
                msg = ""
                print(f"{clientName} has requested details of flight {code}.")

                for flight in json_data['data']:
                    
                    if flight['flight']['iata'] == code.upper():
                        msg += 20*"-" + "\n"
                        msg += f"Flight IATA code: { flight['flight']['iata'] }\n"
                        msg += f"Flight Date: { flight['flight_date'] }\n"
                        msg += f"Departure:\n\tAirport: { flight['departure']['airport'] }\n\tGate: { flight['departure']['gate'] }\n\tTerminal: { flight['departure']['terminal'] }\n"
                        msg += f"Arrival:\n\tAirport: { flight['arrival']['airport'] }\n\tGate: { flight['arrival']['gate'] }\n\tTerminal: { flight['arrival']['terminal'] }\n"
                        msg += f"Flight Status: { flight['flight_status'] }\n"
                        msg += f"Scheduled Departure Time: { flight['departure']['scheduled'] }\n"
                        msg += f"Scheduled Arrival Time: { flight['arrival']['scheduled'] }\n"
                        msg += f"Estimated Arrival Time: { flight['arrival']['estimated'] }\n"
                        msg += f"Delay: { flight['departure']['delay'] } minutes\n"
                        break
                msg += 20*"-" + "\n"
            
            myutils.SendMessage(msg, self.sock)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_p:
    sock_p.bind(server_address)
    sock_p.listen(2)

    threadList = []

    while True:
        if len(threadList) > 2:
            continue

        sock_a, sockname = sock_p.accept()
        obj = MultiThread(sock_a, sockname)
        obj.GenerateThread()