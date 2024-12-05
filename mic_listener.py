import speech_recognition as sr

def mic_listener(queue):
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Configure recognition parameters
    recognizer.pause_threshold = 1.0
    recognizer.phrase_threshold = 0.3
    recognizer.non_speaking_duration = 0.5
    
    while True:
        try:
            # Using microphone as source
            with sr.Microphone(device_index=4) as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio input
                audio = recognizer.listen(
                    source,
                    timeout=None,   # Wait indefinitely
                    phrase_time_limit=None  # No limit on phrase duration
                )
                
                try:
                    # Convert speech to text using Google's API
                    text = recognizer.recognize_google(audio)
                    
                    # If text is recognized, add it to the queue
                    if text and text.strip():
                        # print("Voice command detected:", text)
                        queue.put(("mic", text))
                
                except sr.UnknownValueError:
                    # No speech detected, continue listening
                    continue
                except sr.RequestError:
                    # Network or service error, continue listening
                    continue
        
        except Exception as e:
            print(f"Error in microphone listener: {e}")
            continue
