import json
from response_formatting import format_response

import requests

# def talk_to_llm(system_prompt, user_prompt, conversation_history=None):
#     url = "https://api.perplexity.ai/chat/completions"
    
#     # Initialize messages with system prompt
#     messages = [
#         {
#             "role": "system",
#             "content": f"{system_prompt}"
#         }
#     ]
    
#     # Add conversation history if it exists
#     if conversation_history:
#         messages.extend(conversation_history)
    
#     # Add current user prompt
#     messages.append({
#         "role": "user",
#         "content": f"{user_prompt}"
#     })

#     payload = {
#         "model": "llama-3.1-sonar-huge-128k-online",
#         "messages": messages,
#         "max_tokens": "4000",
#         "temperature": 0.2,
#         "top_p": 0.9,
#         "search_domain_filter": ["perplexity.ai"],
#         "return_images": False,
#         "return_related_questions": False,
#         "search_recency_filter": "month",
#         "top_k": 0,
#         "stream": False,
#         "presence_penalty": 0,
#         "frequency_penalty": 1
#     }
#     headers = {
#         "Authorization": "Bearer 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",
#         "Content-Type": "application/json"
#     }

#     response = requests.request("POST", url, json=payload, headers=headers)
#     response = json.loads(response.text)
#     return response


import os
import openai
# def talk_to_llm(system_prompt, prompt, conversation_history=None):
#     client = openai.OpenAI(
#     api_key="c703d8bda9633193106ece5f87e2e79b6c5998a92b72cc9269428b933ed0441d",
#     base_url="https://api.together.xyz/v1",
#     )

#     messages=[
#         {"role": "system", "content": f"{system_prompt}"}
#     ]
#     # Add conversation history if it exists
#     if conversation_history:
#         messages.extend(conversation_history)

#     user_prompt = prompt["user"]
#     extra_system_prompt = prompt["system"]
#     # Add current user prompt
#     if extra_system_prompt!="":
#         messages.append({
#         "role": "system",
#         "content": f"{extra_system_prompt}"
#     })
#     elif user_prompt!="":
#         messages.append({
#             "role": "user",
#             "content": f"{prompt}"
#         })

#     response = client.chat.completions.create(
#     # model="Qwen/Qwen2.5-72B-Instruct-Turbo",
#     model = "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
#     messages=messages
#     )

#     return response.choices[0].message.content

# import openai

# def talk_to_llm(system_prompt, prompt,tts_model, conversation_history=None):
#     client = openai.OpenAI(
#         api_key="c703d8bda9633193106ece5f87e2e79b6c5998a92b72cc9269428b933ed0441d",
#         base_url="https://api.together.xyz/v1",
#     )

#     messages = [
#         {"role": "system", "content": f"{system_prompt}"}
#     ]
    
#     # Add conversation history if it exists
#     if conversation_history:
#         messages.extend(conversation_history)

#     user_prompt = prompt["user"]
#     extra_system_prompt = prompt["system"]
    
#     # Add current user prompt
#     if extra_system_prompt != "":
#         messages.append({
#             "role": "system",
#             "content": f"{extra_system_prompt}"
#         })
#     elif user_prompt != "":
#         messages.append({
#             "role": "user",
#             "content": f"{prompt}"
#         })

#     # Stream the response
#     response = client.chat.completions.create(
#         model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
#         messages=messages,
#         stream=True  # Enable streaming
#     )

#     # Process streamed chunks as they come in
#     full_response = ""
#     for chunk in response:
#         if chunk.choices[0].text:
#             content_chunk = chunk.choices[0].text
#             full_response += content_chunk
#             print(content_chunk, end="")  # Output each chunk as it arrives
#             # Here you can integrate your voice model to speak the content_chunk

#     return full_response


import openai
from speech_synthesize import run_hinabot

def talk_to_llm(system_prompt, prompt, tts_model, conversation_history=None):
    client = openai.OpenAI(
        api_key="c703d8bda9633193106ece5f87e2e79b6c5998a92b72cc9269428b933ed0441d",
        base_url="https://api.together.xyz/v1",
    )

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

# from prompts import sp_youtube,sp_general
# from speech_synthesize import load_tts_model
# model = load_tts_model()
# prompt = {"system":"","user":"Hey hina, how are you doing? tell me something about yourself"}
# print(talk_to_llm(sp_general, prompt, model, conversation_history=None))