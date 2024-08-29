"""
This script allows you to interact with the Azure OpenAI streaming endpoint via the command line.

Usage:
    python chat-stream.py -e <endpoint> -k <api_key> -m <model>

Arguments:
    -e, --endpoint    Azure OpenAI Endpoint URL from the portal
    -k, --key         Azure OpenAI Access key
    -m, --model       Azure OpenAI model to chat with

Example:
    python chat-stream.py -e https://your-endpoint.openai.azure.com/ -k your-api-key -m your-model

Instructions:
1. Replace <endpoint> with your Azure OpenAI endpoint URL.
2. Replace <api_key> with your Azure OpenAI access key.
3. Replace <model> with the model deployment name you want to use.
4. Run the script from the command line.
5. Type your messages and press Enter to interact with the model.
6. Type "exit" or "quit" to end the chat session.

Note:
- Ensure you have the necessary permissions and access to the Azure OpenAI service.
- Install the required libraries using `pip install openai azure-core`.
"""
import os
import argparse
import openai
from azure.core.exceptions import AzureError

def chat_with_azure_openai(api_endpoint, api_key, model):
    try:
        # Set up the OpenAI API client
        openai.api_type = "azure"
        openai.azure_endpoint = api_endpoint
        openai.api_key = api_key
        openai.api_version = "2024-07-01-preview"

        # Initialize chat history
        messages = []

        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting chat...")
                break

            # Append user message to chat history
            messages.append({"role": "user", "content": user_input})

            # Send the request to the Azure OpenAI streaming endpoint
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.9,
                stream=True
                #,stream_options={"include_usage": True}
            )

            # Stream the response
            print("Azure OpenAI: ", end="")
            assistant_message = ""
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta:
                    content = chunk.choices[0].delta.content
                    if content:
                        print(content, end="", flush=True)
                        assistant_message += content
            print()
            # Append assistant message to chat history
            messages.append({"role": "assistant", "content": assistant_message})

    except AzureError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat with Azure OpenAI')
    parser.add_argument('-e', '--endpoint', help='Azure OpenAI Endpoint URL from the portal', required=True)
    parser.add_argument('-k', '--key', help='Azure OpenAI Access key', required=True)
    parser.add_argument('-m', '--model', help='Azure OpenAI model to chat with', required=True)
    args = parser.parse_args()

    chat_with_azure_openai(args.endpoint, args.key, args.model)