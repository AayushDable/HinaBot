def format_response(response_text):
    # Split the response into chat and code parts
    parts = response_text.split("```python\n")
    if len(parts) == 2:
        chat_text = parts[0].strip()
        code_text = parts[1].strip()
        
        # Format for code execution
        # code_block = code_text.strip('`python').strip('`').strip()
        
        return {
            "speech": chat_text,
            "code": code_text
        }
