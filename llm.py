import json
from response_formatting import format_response
import requests
import os
import openai
from speech_synthesize import run_hinabot

def talk_to_llm(system_prompt, prompt, tts_model, conversation_history=None):
    client = openai.OpenAI()

    messages = [
        {"role": "system", "content": f"{system_prompt}"}
    ]
    
    # Add conversation history if it exists
    if conversation_history:
        messages.extend(conversation_history)

    user_prompt = prompt["user"]
    extra_system_prompt = prompt["system"]
    
    # Add current user prompt
    if extra_system_prompt != "":
        messages.append({
            "role": "system",
            "content": f"{extra_system_prompt}"
        })
    elif user_prompt != "":
        messages.append({
            "role": "user",
            "content": f"{prompt}"
        })

    # Stream the response
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        messages=messages,
        stream=True  # Enable streaming
    )

    full_response = ""
    buffer = ""
    inside_code_block = False

    # List of sentence-ending punctuation marks
    sentence_breakers = ['.', '?', '!', '...']
    combined=[]

    for chunk in response:
        if chunk.choices[0].text:
            content_chunk = chunk.choices[0].text
            full_response += content_chunk
            buffer += content_chunk

            # Check for start or end of code block
            if "```" in buffer:
                inside_code_block = not inside_code_block  # Toggle code block state
                buffer = ""  # Reset buffer when entering/exiting code block
                continue  # Skip sending anything to TTS while in code block

            # Only process text outside of code blocks
            if not inside_code_block:
                sentences = []
                temp_sentence = ""

                for char in buffer:
                    temp_sentence += char

                    # If we encounter a sentence breaker and there is meaningful content before it
                    if char in sentence_breakers and len(temp_sentence.strip()) > 1:
                        sentences.append(temp_sentence.strip())
                        temp_sentence = ""
                        buffer = ""

                # Send complete sentences to TTS model
                
                for sentence in sentences:  # All but the last part (which may be incomplete)
                    if len(sentence) > 1:
                        combined.append(sentence)
                        sentences.pop()
                        if len(combined) >= 5:  # Ensure it's not just a punctuation mark
                            current_statement = ' '.join(combined)
                            print(current_statement)
                            run_hinabot(tts_model, current_statement)
                            combined=[]

    if len(combined) > 0:
        current_statement = ' '.join(combined)
        print(current_statement)
        run_hinabot(tts_model, current_statement)
   

    return full_response
