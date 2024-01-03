# this is an example of how to use completions and chat with the openai library beyond the 1.x release
# as of the 1.x library release, the chat endpoint is not available, but the completions endpoint is
# you should switch to use the lastest stable calls in your code
# https://beta.openai.com/docs/api-reference/chat
# pip install -r ./requirements.txt or with pyenv - pyenv exec pip install -r ./requirements.txt
# python .\chat-1x.py -e <endpoint> -k <key> -m <modelDeployment>
# note Functions will only work with 1106 and later Model Versions only.
# to get the weather ask about the weather in a predefined city "What is the weather in San Francisco?"
# Note this is using a stub and does not go to the weather API. You can change the stub to call the weather API

import os
import json
from openai import AzureOpenAI
import argparse
from azure.core.exceptions import AzureError



if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Chat with Azure Open AI')
    parser.add_argument('-e', '--endpoint', help='Azure OpenAI Endpoint URL from the portal', required=True)
    parser.add_argument('-k', '--key', help='Azure Open AI Access key', required=True)
    parser.add_argument('-m', '--modelDeployment', help='Azure Open AI model to chat with', required=True)
    parser.add_argument('-f', '--useFunction', help='Azure Open AI function Json', required=False, type=bool, default=False)
    args = parser.parse_args()
    apiKey = args.key
    apiEndpoint = args.endpoint
    model = args.modelDeployment
    useFunction = args.useFunction

    def get_current_weather(location, unit="fahrenheit"):
        """Get the current weather in a given location"""
        if "tokyo" in location.lower():
            return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
        elif "san francisco" in location.lower():
            return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
        elif "paris" in location.lower():
            return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
        else:
            return json.dumps({"location": location, "temperature": "unknown"})

    client = AzureOpenAI(
        api_key = apiKey,  
        api_version = "2023-12-01-preview",
        azure_endpoint = apiEndpoint
    )
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ]
    

    messages = [{"role": "system", "content": "Your name is Azure Andy and you ar an assistant that is a large language model trained by OpenAI to run on Azure."}]
    print("Welcome to Azure Andy, the Azure OpenAI Chatbot")
    print("You can ask me questions about the weather, or ask me to do things for you.")
    print("Type 'quit' to exit the chat.")
    print("\n")
    while True:
        message = input("Your question: ")
        if message == "quit"  or message == "exit":
            exit()
        messages.append({"role": "user", "content": message})
        if (useFunction):
            response = client.chat.completions.create(
                model=model, 
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )
        else:
            response = client.chat.completions.create(
                model=model, 
                messages=messages,
            )
        #print(response.model_dump_json(indent=2))
        print("\n")
        print("Response:\n")
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if tool_calls:
            available_functions = {
                "get_current_weather": get_current_weather,
                } 
            #print(response_message.model_dump_json(indent=2))
            messages.append({"content": response_message.content,
                "role": response_message.role,
                "tool_calls":response_message.tool_calls,
                })
            for tool_call in tool_calls:

                function_name  = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args  = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    location=function_args.get("location"),
                    unit=function_args.get("unit"),
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
                function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
                )
            #print(messages)
            second_response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            print(second_response.choices[0].message.content)
            print("\n\n")
            messages.append({"role": "assistant", "content": second_response.choices[0].message.content})    
        else:
            print(response_message.content)
            print("\n\n")
            messages.append({"role": "assistant", "content": response_message.content})