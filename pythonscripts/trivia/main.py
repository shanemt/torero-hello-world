import requests
import argparse
import os

def read_system_prompt(prompt_file):
    prompts_dir = "./prompts/"
    file_path = os.path.join(prompts_dir, prompt_file)
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: Prompt file '{prompt_file}' not found in {prompts_dir}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Send a message to ChatGPT API and get a response")
    parser.add_argument("--message", required=True, help="The message to send to ChatGPT")
    parser.add_argument("--system_prompt", help="Filename of the system prompt in ./prompts/ directory", default="trivia.txt")
    parser.add_argument("--openapi_api_key", help="Filename of the system prompt in ./prompts/ directory")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        api_key = args.open_api_key
        if not api_key:
            print("Error: OPENAI_API_KEY environment variable or argument is not set")
            return

    system_prompt = read_system_prompt(args.system_prompt)
    if system_prompt is None:
        return

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.message}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        print(result['choices'][0]['message']['content'])
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()