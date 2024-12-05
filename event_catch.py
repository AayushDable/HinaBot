def mic_or_bluetooth_event_catcher(queue):
    """
    Central event handler that catches events from both mic and Bluetooth listeners.
    """
    print("Listening..")
    while True:
        try:
            event_source, message = queue.get()  # Get an event from the queue

            if event_source == "mic":
                print("Processing..")
                return message

            elif event_source == "bluetooth":
                print("Processing..")
                return message

        except Exception as e:
            print(f"Error in event catcher: {e}")