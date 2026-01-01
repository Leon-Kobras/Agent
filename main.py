import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import *

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    for _ in range(4):
        response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        
        if response.candidates != []:
            for items in response.candidates:
                messages.append(items.content)
        if not response.function_calls:
            break
            
        
        for item in response.function_calls:
            function_call_result = call_function(item, args.verbose)
            if function_call_result.parts == []:
                raise Exception("Error")
            if function_call_result.parts[0].function_response == None:
                raise Exception("Error")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Error")
            
            if args.verbose == True:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(function_call_result)
    print("DEBUG function_calls:", response.function_calls)
    print("Final Response:")
    print(response.text)
if __name__ == "__main__":
    main()
