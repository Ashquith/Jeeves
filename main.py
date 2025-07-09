import sys
import os
from google import genai
from dotenv import load_dotenv
from google.genai import types

def main():
    load_dotenv()

    if len(sys.argv) <2:
        sys.exit(1)
    if "--verbose" in sys.argv:
        input_text = " ".join(sys.argv[1:-1])
        verbose = True
    else:
        input_text = " ".join(sys.argv[1:])
        verbose = False
    
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables or .env file.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=input_text)]),
    ]
    
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
    )

    if verbose:
        print(f"User prompt: {input_text}")
        print(f"Response: {response.text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(f"Response: {response.text}")



if __name__ == "__main__":
    main()
