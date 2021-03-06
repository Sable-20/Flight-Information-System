import socket
import myutils
import sys


print(10*"-" + "Flight Information System" + 10*"-")
server_address = ("127.0.0.1", 59420)

name = input("Enter your name: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(server_address)
    sock.settimeout(5)

    # verify if server accepted connection
    try:
        myutils.ReceiveMessage(sock)
    except Exception as err:
        print("Connection request timed out. The server might be overloaded, try again later.\nQuitting application.\n\n " + err)
        sys.exit()
        
    myutils.SendMessage(name.strip(), sock)

    # loop of death aka infinite while loop
    while True:
        airportCode = input("Enter an airport code (icao): ")
        myutils.SendMessage(airportCode.strip(), sock)

        print("\nAvailable options:")
        print("arrived                      - Displays a list of arrived flights at the selected airport.")
        print("delayed                      - Displays a list of delayed flights at the selected airport.")
        print("city {city_iata_code}        - Displays all flights coming from a specific city {city_iata_code} to the selected airport.")
        print("details {flight_iata_code}   - Displays details of a selected flight {flight_iata_code}.")
        print("quit                         - Disconnects from the server and closes application.\n")

        choice = input("Choose an option: ")
        choice = choice.lower().strip()

        # more logic checking if they quit... etc
        if choice == 'quit':
            myutils.SendMessage(choice, sock)
            break

        elif choice == 'arrived':
            myutils.SendMessage(choice, sock)
            msg = myutils.ReceiveMessage(sock)
            print(f"Arrived flights at airport {airportCode}: ")
            print(msg)

        elif choice == 'delayed':
            myutils.SendMessage(choice, sock)
            msg = myutils.ReceiveMessage(sock)
            print(f"Delayed flights at airport {airportCode}: ")
            print(msg)

        elif choice.startswith("city ") and len(choice) == 8:
            myutils.SendMessage(choice, sock)
            city = choice[5:]
            msg = myutils.ReceiveMessage(sock)

            print(f"Flights coming from city {city}: ")
            print(msg)

        elif choice.startswith("details ") and len(choice) >= 13:
            myutils.SendMessage(choice, sock)
            flight = choice[8:]
            msg = myutils.ReceiveMessage(sock)

            print(f"Details of flight {flight}:")
            print(msg)
            
        # this is here cause in QA they try everything but what actually breaks things
        else:
            print("Option not available or wrong use of syntax.")
    