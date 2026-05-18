import os
import sys
import json
import base64
from openai import OpenAI
from pathlib import Path

client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy123")
MAX_INLINE_TEXT_CHARS = 15000
MAX_FILE_SIZE_MB = 5

def should_upload_directly(file_path, extracted_text=None):
    ext = Path(file_path).suffix.lower()

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        return True

    complex_formats = [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".docx"]

    if ext in complex_formats:
        return True

    if extracted_text and len(extracted_text) > MAX_INLINE_TEXT_CHARS:
        return True

    return False

def build_prompt(prompt, dummy_json, extracted_text=None):
    final_prompt = f"""
    {prompt}

    ====================
    DUMMY JSON VALUES
    ====================

    {dummy_json}

    ====================
    TASK
    ====================

    1. Extract all PII values from the document.
    2. Compare extracted values with dummy JSON values.
    3. Return ONLY values missing from dummy JSON.
    4. Return response STRICTLY in JSON format.
    5. Do not return explanation.
    """

    if extracted_text:
        final_prompt += f"""

        ====================
        DOCUMENT TEXT
        ====================

        {extracted_text}
        """

    return final_prompt

def extract_text_from_file(file_path):
    text = ""
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
        text = file_content.strip()
    return text    

def extract_text_from_json(json_path):
    text = ""
    with open(json_path,"r", encoding="utf-8") as file:
        text = json.load(file)    
    return text

def verify_with_llm(file_path,dummy_json,prompt,extracted_text=None):
    try:
        is_upload_directly = should_upload_directly(file_path, extracted_text)

        final_prompt  = build_prompt(prompt, dummy_json, None if is_upload_directly else extracted_text)

        if is_upload_directly:
            print("Uploading file directly to LLM")
            with open(file_path, "rb") as file:
                txt_bytes = file.read()
            txt_b64 = base64.b64encode(txt_bytes).decode("utf-8")    
            response = client.chat.completions.create(
            model="catgpt-browser",
            messages=[
                {
                 "role": "user",
                 "content": [
                        {"type": "text", "text": final_prompt},
                        {"type": "file", "file": {"filename": file_path, "data": txt_b64,"mime_type": "text/plain"}}
                    ]
                }
            ]
        )
        else:
            print("Sending extracted text in prompt to LLM")
            response = client.chat.completions.create(
                model="catgpt-browser",
                messages=[
                    {
                    "role": "user",
                    "content": final_prompt
                    }
                ]
            )

        content = response.choices[0].message.content
        return content  
    except Exception as e:
        print(f"LLM Error: {e}")
        return None    

def main():
    if len(sys.argv) < 2:
        print("Filepath not found in CLI")
        sys.exit(1)

    file_path = sys.argv[1]

    extracted_text = extract_text_from_file(file_path)

    dummy_json = extract_text_from_json("dummy_values.json")

    prompt = f""" 
        You are a document intelligence assistant.

        Extract all names, hospital/facility names, street addresses, city, zip code, dates of birth, emails, phone numbers, social security numbers, medical record numbers, and insurance IDs. For person or hospital or facility or street names, partial names also should be detected.

        you will be given text or attached text file and a set of values your task is to check if any of the extracted values are not present in the list and only return those values.
    """

    response = verify_with_llm(
        file_path=file_path,
        dummy_json=dummy_json,
        prompt=prompt,
        extracted_text=extracted_text
    )
    
    print("response ==> ",response)

    return 

if __name__ == "__main__":
    main()