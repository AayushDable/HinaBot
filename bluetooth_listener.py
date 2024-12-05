import bluetooth
import time

def bluetooth_listener(queue):
    """
    Starts a Bluetooth server that listens for messages.
    When a message is received, it is passed to the `queue`.
    If the connection is lost, it waits for reconnection.
    """
    while True:
        try:
            # Create a Bluetooth socket using RFCOMM protocol
            server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

            # Bind to any available Bluetooth adapter and use a dynamic port (PORT_ANY)
            port = bluetooth.PORT_ANY
            server_sock.bind(("", port))
            server_sock.listen(1)

            print(f"Waiting for connection on RFCOMM channel {port}")

            # Make the service discoverable by clients using the SPP UUID
            uuid = "00001101-0000-1000-8000-00805F9B34FB"
            bluetooth.advertise_service(server_sock, "BluetoothServer",
                                        service_id=uuid,
                                        service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                        profiles=[bluetooth.SERIAL_PORT_PROFILE])

            # Accept an incoming connection
            client_sock, client_info = server_sock.accept()
            print(f"Accepted connection from {client_info}")

            while True:
                try:
                    # Receive data from the client (Android app)
                    data = client_sock.recv(1024)  # Buffer size is 1024 bytes
                    if not data:
                        break  # Client disconnected

                    decoded_message = data.decode('utf-8')
                    print("Bluetooth message received:", decoded_message)

                    # Add the received Bluetooth message to the queue
                    queue.put(("bluetooth", decoded_message))

                except OSError as e:
                    print(f"Error in Bluetooth listener (client disconnected): {e}")
                    break  # Exit inner loop and go back to waiting for reconnection

        except OSError as e:
            print(f"Error in Bluetooth listener (server socket): {e}")

        finally:
            # Close sockets after disconnection or error
            if 'client_sock' in locals():
                client_sock.close()
            if 'server_sock' in locals():
                server_sock.close()

        print("Connection lost. Waiting for reconnection...")
        time.sleep(2)  # Wait before attempting to reconnect
