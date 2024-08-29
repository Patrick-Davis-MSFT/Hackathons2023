import azure.functions as func
import datetime
import json
import logging
import tiktoken
import io

app = func.FunctionApp()
model = ""
@app.route(route="promptCounter/{subscription}", auth_level=func.AuthLevel.FUNCTION)
def promptCounter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('promptCounter HTTP trigger function processed a request.')

    # Get the subscription parameter from the route
    subscription = req.route_params.get('subscription')
    logging.info(f"Subscription: {subscription}")
    try:
        req_body = req.get_json()
        logging.info(f"Request body: {req_body}")
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON in request body.",
            status_code=400
        )

    messages = req_body.get('messages') if req_body else None
    model = req_body.get('model') if req_body else None
    
    logging.info(f"messages: {messages}")
    logging.info(f"model: {model}")

    if messages:
        num_tokens = num_tokens_from_messages(messages=messages, model=model)
        logging.info(f"reported tokens from user prompt: {num_tokens}")
        return func.HttpResponse(
            json.dumps({"token_count": num_tokens}),
            status_code=200,
            mimetype="application/json"
        )
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the request body for a personalized response.",
             status_code=200
        )

def getOutputStream(req: func.HttpRequest):
    assistant_message = ""
    try:
        logging.info("Try to get Stream message")
        req_body_stm = req.get_body().decode('utf-8') 
        # Split the body by newlines and process each line
        for line in req_body_stm.split('\n'):
            if line.startswith('data: '):
                json_data = line[len('data: '):]
                try:
                    chunk = json.loads(json_data)
                    if chunk.get('choices') and chunk['choices'][0].get('delta'):
                        content = chunk['choices'][0]['delta'].get('content')
                        if chunk['model']: 
                            model = chunk['model']
                        if content:
                            print(content, end="", flush=True)
                            assistant_message += content
                
                except json.JSONDecodeError as e:
                    logging.error(f"Failed to parse JSON: {e}")
        logging.info(f"assistant_message: {assistant_message}")
    except:
        logging.info("Failed to get Stream message")
    return assistant_message

def getOutputBulk(req: func.HttpRequest):
    assistant_message = ""
    try:
            logging.info("Try to get bulk message")
            req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON in request body.",
            status_code=400
        )

    choices = req_body.get('choices') if req_body else None
    model = req_body.get('model') if req_body else None
    
    logging.info(f"choices: {choices}")
    logging.info(f"model: {model}")

    if choices and isinstance(choices, list) and len(choices) > 0:
        assistant_message = choices[0].get('message', {}).get('content', "")
        logging.info(f"bulk messages: {assistant_message}")
    return assistant_message

@app.route(route="pmtCntOutBulk/{subscription}", auth_level=func.AuthLevel.FUNCTION)
def pmtCntOutBulk(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('promptCounterOutBulk HTTP trigger function processed a request.')
    
    # Get the subscription parameter from the route
    subscription = req.route_params.get('subscription')
    logging.info(f"Subscription: {subscription}")
    assistant_message = ""
    # Read the MIME type of the request
    assistant_message = getOutputStream(req)
    if assistant_message =="":
        assistant_message = getOutputBulk(req)
        
    logging.info(f"assistant_message main function: {assistant_message}")
    if assistant_message:
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(assistant_message))
        logging.info(f"reported tokens from response: {num_tokens}")
        return func.HttpResponse(
            json.dumps({"token_count": num_tokens}),
            status_code=200,
            mimetype="application/json"
        )
    return func.HttpResponse(
        "This HTTP triggered function executed successfully. Pass a name in the request body for a personalized response.",
        status_code=200
    )




def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    elif "gpt-4o" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4o-2024-05-13")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
