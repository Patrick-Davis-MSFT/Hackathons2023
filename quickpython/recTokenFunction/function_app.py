import azure.functions as func
import datetime
import json
import logging
import tiktoken
import io
import requests
import hashlib
import hmac
import base64
import os

app = func.FunctionApp()
model = ""
workspace_id = os.getenv('LOG_ANALYTICS_WORKSPACE_ID','NEED LOG_ANALYTICS_WORKSPACE_ID')
primary_key = os.getenv('LOG_ANALYTICS_PRIMARY_KEY', 'NEED LOG_ANALYTICS_PRIMARY_KEY')
log_type = 'CustomUsageLog'

def send_to_log_analytics(workspace_id, primary_key, log_type, json_data):
    customer_id = workspace_id
    shared_key = primary_key

    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(json_data)

    signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)
    uri = f'https://{customer_id}.ods.opinsights.azure.com{resource}?api-version=2016-04-01'

    headers = {
        'Content-Type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }

    response = requests.post(uri, headers=headers, data=json_data)
    if response.status_code >= 200 and response.status_code <= 299:
        print('Accepted')
    else:
        print(f"Response code: {response.status_code}")

def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
    x_headers = f'x-ms-date:{date}'
    string_to_hash = f'{method}\n{content_length}\n{content_type}\n{x_headers}\n{resource}'
    bytes_to_hash = bytes(string_to_hash, encoding='utf-8')
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode('utf-8')
    authorization = f'SharedKey {customer_id}:{encoded_hash}'
    return authorization

@app.route(route="promptCounter/{subscription}", auth_level=func.AuthLevel.FUNCTION)
def promptCounter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('promptCounter HTTP process incoming request.')
    logObj = {}
    # Get the subscription parameter from the route
    subscription = req.route_params.get('subscription')
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON in request body.",
            status_code=400
        )

    messages = req_body.get('messages') if req_body else None
    model = req_body.get('model') if req_body else None
    
    if messages:
        num_tokens = num_tokens_from_messages(messages=messages, model=model)
        logging.info(f"reported tokens from user prompt: {num_tokens}")
        logObj["estimated_token_count"] = num_tokens
        logObj["subscription"] = subscription
        logObj["model"] = model
        logObj["direction"] = 'toAOAI'
        logObj["stream"] = req_body.get('stream')
        # Send usage data to Log Analytics
        send_to_log_analytics(workspace_id, primary_key, log_type, json.dumps(logObj))
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
    model = ""
    retValue = {}
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
    except:
        logging.info("Failed to get Stream message")

    retValue["assistant_message"] = assistant_message
    retValue["model"] = model
    return retValue

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
    

    if choices and isinstance(choices, list) and len(choices) > 0:
        assistant_message = choices[0].get('message', {}).get('content', "")
    return assistant_message

@app.route(route="pmtCntOut/{subscription}", auth_level=func.AuthLevel.FUNCTION)
def pmtCntOut(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('promptCounterOutBulk HTTP process outbound request.')
    logObj = {}
    stream = True
    # Get the subscription parameter from the route
    subscription = req.route_params.get('subscription')
    assistant_message = ""
    # Read the MIME type of the request
    outStreamRes = getOutputStream(req)
    if outStreamRes:
        assistant_message = outStreamRes.get("assistant_message")
        model = outStreamRes.get("model")

    if assistant_message =="":
        assistant_message = getOutputBulk(req)
        stream = False
        try: 
            req_body = req.get_json()
            if req_body.get('usage'):
                usage = req_body.get('usage')
                model = req_body.get('model')
                if usage:
                    logObj=usage
        except:
            logging.info("Failed to get usage")
        
    if assistant_message:
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(assistant_message))
        logging.info(f"reported tokens from response: {num_tokens}")

        logObj["estimated_token_count"] = num_tokens
        logObj["subscription"] = subscription
        logObj["model"] = model
        logObj["direction"] = 'fromAOAI'
        logObj["stream"] = stream
        # Send usage data to Log Analytics
        send_to_log_analytics(workspace_id, primary_key, log_type, json.dumps(logObj))
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
    except:
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
