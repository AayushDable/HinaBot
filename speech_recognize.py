import speech_recognition as sr

# def listen_for_command():
#     # Initialize recognizer
#     recognizer = sr.Recognizer()
    
#     # Configure recognition parameters
#     recognizer.pause_threshold = 1.0  # Increase pause threshold to wait longer between phrases
#     recognizer.phrase_threshold = 0.3  # Minimum seconds of speaking audio before we consider the speaking audio a phrase
#     recognizer.non_speaking_duration = 0.5  # Seconds of non-speaking audio to keep on both sides of the recording
    
#     # Using microphone as source
#     with sr.Microphone(device_index=4) as source:
#         print("Listening...")
#         # Adjust for ambient noise
#         recognizer.adjust_for_ambient_noise(source, duration=0.5)
#         # Listen for audio input with modified timeout and phrase time limit
#         try:
#             audio = recognizer.listen(
#                 source,
#                 timeout=None,  # Maximum seconds to wait for a phrase to start
#                 phrase_time_limit=None  # Maximum seconds for a phrase. None means no limit
#             )
            
#             # Convert speech to text using Google's API
#             text = recognizer.recognize_google(audio)
#             return text
#         except sr.WaitTimeoutError:
#             print("Listening timed out. No speech detected.")
#             return None
#         except sr.UnknownValueError:
#             return None
#         except sr.RequestError as e:
#             return None

def listen_for_command():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Configure recognition parameters
    recognizer.pause_threshold = 1.0
    recognizer.phrase_threshold = 0.3
    recognizer.non_speaking_duration = 0.5
    print("Listening...")
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
                    
                    # If text is recognized, return it
                    if text and text.strip():
                        print("Processing..")
                        return text
                
                except sr.UnknownValueError:
                    # No speech detected, continue listening
                    continue
                except sr.RequestError:
                    # Network or service error, continue listening
                    continue
        
        except Exception:
            # Any other unexpected error, continue listening
            continue