from prompts import sp_youtube,sp_general
from llm import talk_to_llm
from speech_synthesize import load_tts_model,run_hinabot
from response_formatting import format_response
from execute_python_code import exec_python
# from youtube_surfer import search_youtube
from speech_recognize import listen_for_command
import multiprocessing
from mic_listener import mic_listener
from bluetooth_listener import bluetooth_listener
from event_catch import mic_or_bluetooth_event_catcher

def main():
    speech_model = load_tts_model()
    conversation_history = []  # Initialize conversation history
    missing_packages = []
    package_success = False
    other_error_statements = False
    code_success_statements = False

    queue = multiprocessing.Queue()

    # Start microphone listener in a separate process
    mic_process = multiprocessing.Process(target=mic_listener, args=(queue,))
    
    # Start Bluetooth listener in a separate process
    bt_process = multiprocessing.Process(target=bluetooth_listener, args=(queue,))
    
    mic_process.start()
    bt_process.start()

    print("Listening on both bluetooth and mic channels!")
    while True:
        if code_success_statements:
            query = {"system":f"System alert: Your attempt at running the code/task completed successfully! Here are the print statements {code_success_statements}. you can continue with the task, if it hasn't been completed yet. Exception: If task was home automation, do not bother the user with a confirmation response","user":""}
            
            code_success_statements=False
        elif package_success:
            query = {"system":f"System alert: Your attempt at installed the package/s was success. Please ask the user if they would like you to run the previous code (prior to package installation) again","user":""}
            package_success = False
        elif other_error_statements:
            query = {"system":f"System alert: Your previous code failed due to an error. {other_error_statements}. If you are confident at fixing this, provide very briefly (1-2 short phrases) your idea to fix it to user, and then perform the fix. If you see this message many times. Stop trying and ask user if you should try again or stop.","user":""}
            other_error_statements = False
        elif missing_packages:
            query = {"system":f"System alert: Your previous code failed due to missing_packages:{missing_packages}. Please ask the user if you should install the package. if they say yes, kindly generate the pip commands in your code block","user":""}
            missing_packages = []
        else:
            query = {"system":"","user":mic_or_bluetooth_event_catcher(queue)}
        if query["system"] not in ["",None] or query["user"] not in ["",None]:
            # Get response with conversation history
            response = talk_to_llm(sp_general, query, speech_model, conversation_history)
            # text_response = response['choices'][0]['message']['content']
            text_response = response
            
            # Add the user query and assistant's response to history
            if query["system"]!="":
                conversation_history.append({
                    "role": "system",
                    "content": query["system"]
                })
            
            elif query["user"]!="":
                conversation_history.append({
                    "role": "user",
                    "content": query["user"]
                })

            conversation_history.append({
                "role": "assistant",
                "content": text_response
            })
            
            # Keep conversation history to a reasonable size (last 10 messages)
            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]
            
            response_dict = format_response(text_response)

            if response_dict == '' or response_dict is None:
                # run_hinabot(speech_model, text_response)
                continue
            
            # if response_dict["speech"]!='':
            #     run_hinabot(speech_model, response_dict["speech"])

            exec_response = exec_python(response_dict["code"])

            if exec_response['type'] == 'success':
                code_success_statements=exec_response['output']

            elif exec_response['type'] == 'package_installation_success':
                package_success = True

            elif exec_response['type'] == 'missing_packages':
                missing_packages = exec_response['errors']

            elif exec_response['type'] == 'error':
                other_error_statements = exec_response['errors']

            if missing_packages:
                if missing_packages[0] == "success":
                    package_success = True

if __name__ == "__main__":
    # Start the main loop
    main()