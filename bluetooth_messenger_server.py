import bluetooth

def bluetooth_listener(queue):
    """
    Starts a Bluetooth server that listens for messages.
    When a message is received, it is passed to the `queue`.
    """
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    port = bluetooth.PORT_ANY
    server_sock.bind(("", port))
    server_sock.listen(1)

    print(f"Waiting for connection on RFCOMM channel {port}")

    uuid = "00001101-0000-1000-8000-00805F9B34FB"
    bluetooth.advertise_service(server_sock, "BluetoothServer",
                                service_id=uuid,
                                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE])

    client_sock, client_info = server_sock.accept()
    print(f"Accepted connection from {client_info}")

    try:
        while True:
            data = client_sock.recv(1024)  # Buffer size is 1024 bytes
            if not data:
                break

            decoded_message = data.decode('utf-8')
            print("Bluetooth message received:", decoded_message)

            # Add the received Bluetooth message to the queue
            queue.put(("bluetooth", decoded_message))

            client_sock.send("Message received")

    except OSError as e:
        print(f"Error in Bluetooth listener: {e}")

    client_sock.close()
    server_sock.close()


# # Example usage of the Bluetooth server with a callback function
# def bluetooth_received_message(message):
#     """
#     This function will be called whenever a message is received from the client.
#     """
#     print(f"Handling received message: {message}")
#     return {"system":"","user":message}
#     # Here you can process or return this message to another part of your program.
    
# if __name__ == "__main__":
#     start_bluetooth_server(bluetooth_received_message)
