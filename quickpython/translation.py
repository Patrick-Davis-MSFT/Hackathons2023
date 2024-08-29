import requests, uuid, json

# Replace 'YOUR_TRANSLATOR_TEXT_SUBSCRIPTION_KEY' and 'YOUR_TRANSLATOR_TEXT_ENDPOINT' with your Azure Translator Text subscription key and endpoint
subscription_key = ''
endpoint = ''

# The path for the Translate API
path = '/translate?api-version=3.0'

# Function to translate text
def translate_text(text, target_language):
    constructed_url = endpoint + path + '&to=' + target_language

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': 'USGov Virginia',  # Replace with your resource region
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    response = requests.post(constructed_url, headers=headers, json=body)
    result = response.json()

    return result[0]['translations'][0]['text']

# Main loop
if __name__ == "__main__":
    target_language = input("Enter the target language code ( 'es'->Spanish\n'zh-Hans'->Chinese Simplified\n'ru'->Russian\n'ru'->Hindi): ")
    while True:
        user_input = input("Enter text to translate (or type 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        translated_text = translate_text(user_input, target_language)
        print("Translated text:", translated_text)