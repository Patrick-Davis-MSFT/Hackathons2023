import csv
import json
from openai import AzureOpenAI
from azure.core.exceptions import AzureError
import sys
import requests

#downloaded the Airports CSV from https://openflights.org/data.php
pathtoairport = 'quickpython/Airports/airports.csv'

def search_csv(file_path:str = pathtoairport, airport_code:str = ''):
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["IATA"] == airport_code:
                retVal = json.dumps({"lat": row["LATITUDE"], "long": row["LONGITUDE"]})
                return retVal
    return None

def get_lat_long_weather(obj={}):
    latitude = str(obj.get('latitude'))
    longitude = str(obj.get('longitude'))
    response = requests.get(f'https://api.weather.gov/points/{latitude},{longitude}')
    unit="fahrenheit"
    if response.status_code == 200:
         # Parse the response as JSON
        data = response.json()
        #print(data)
        office = data.get("properties",{}).get("gridId")
        gridx = data.get("properties",{}).get("gridX")
        gridy = data.get("properties",{}).get("gridY")

        #print(office)
        #print(gridx)
        #print(gridy)
        # Make a request to the /gridpoints/{office}/{gridX},{gridY}/forecast endpoint
        response = requests.get(f'https://api.weather.gov/gridpoints/{office}/{gridx},{gridy}/forecast')
        if response.status_code == 200:
            # Parse the response as JSON
            data = response.json()
            #print(data)
            # Get the current temperature
            temperature = data.get("properties",{}).get("periods", [])[0].get("temperature")
            detailedForecast = data.get("properties",{}).get("periods", [])[0].get("detailedForecast")
            name = data.get("properties",{}).get("periods", [])[0].get("name")
            #print(temperature)
            # Return the temperature
            return data.get("properties",{}).get("periods", [])
        else:
            print(f"Request failed with status code step 2 {response.status_code}")

    else:
        print(f"Request failed with status code step 1 {response.status_code}")


    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_lat_long_weather",
                "description": "Get the current weather in a given location though latitude and longitude",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "latitude": {
                            "type": "string",
                            "description": "the latitude of the airport",
                        },
                        "longitude": {
                            "type": "string",
                            "description": "the longitude of the airport",
                        }
                    },
                    "required": ["latitude","longitude"],
                },
            },
        },
         {
            "type": "function",
            "function": {
                "name": "search_csv",
                "description": "gets the latitude and logitude of an airport based on the current IATA airport code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "the CSV file path to search. This is optional and defaults to the airports.csv file",
                        },
                        "airport_code": {
                            "type": "string",
                            "description": "the three letter IATA airport code",
                        }
                    },
                    "required": ["airport_code"],
                },
            },
        }
    ]
    systemPrompt = """You are a TAF builder assistant. 
    Given an IATA Airport code create the TAF based on the most recent weather data. 
    Use the search_csv to get the latitude and longitude of the airport IATA code provided. 
    Use the data returned from the get_lat_long_weather function as the weather data. 
    Only respond with a TAF for the IATA Airport code provided. Do NOT guess or assume airport locations or weather data. 
    If only provided a IATA assume the user is requesting a TAF for that airport and .
    If requested to provide anything else other than a TAF, respond with an error message and a warning."""