import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_research(user_topic):
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY environment variable not set.")

    # Internal prompt for finance research, provided as a system message.
    internal_prompt = (
        "Please provide detailed research with an emphasis on finance, "
        "including investment banking, consulting, venture capital, and related topics."
    )

    # Build the payload according to Perplexity's API documentation.
    payload = {
        "model": "sonar", # sonar-reasoning-pro
        "messages": [
            {"role": "system", "content": internal_prompt},
            {"role": "user", "content": user_topic}
        ],
        "max_tokens": 123,
        "temperature": 0.2,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1,
        "response_format": None
    }

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    url = "https://api.perplexity.ai/chat/completions"

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

    result_json = response.json()
    try:
        # Assuming the answer is contained in choices[0].message.content.
        research = result_json['choices'][0]['message']['content']
    except (KeyError, IndexError):
        research = "No valid result found in the API response."

    return research

if __name__ == "__main__":
    user_topic = input("Enter your research topic related to finance: ")
    result = get_research(user_topic)
    print("\nFinal Research Result:")
    print(result)