from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from pyngrok import ngrok
from fastapi.middleware.cors import CORSMiddleware
import json
import nest_asyncio
from Custom_promotion.custom_promotion import get_promotion
from Custom_promotion.load_csv_file import load_csv
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

origins = ["*"]

# Adding Cross-Origin Resource Sharing (CORS) middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Pydantic BaseModel for input parameters related to property details
class model_input(BaseModel):
    Name: str
    Location: str
    PropertyType: str
    Availability: str
    PriceRange: str
    Amenities: str
    Description: str
    TargetedAudience: str

@app.get("/")
def welcome():
    """
    Returns a dictionary containing the key-value pair "hello": "world".

    Returns:
        dict: A dictionary with the key "hello" and value "world".
    """
    return {"Hello":"Welcome to Custome Promotion Campaing System"}


@app.post('/property')
def prop_detail(input_parameters: model_input):
    """
    Processes input parameters to extract property details and generates a promotion for the targeted audience.

    Args:
        input_parameters (model_input): An object containing property details in JSON format.

    Returns:
        str: A str containing the promotion details tailored to the targeted audience.
    """
    try:
        logging.info(f"Received input parameters")

        input_data = input_parameters.json()
        input_dictionary = json.loads(input_data)
        
        property_details = {"Name": input_dictionary['Name'], "Location": input_dictionary['Location'],
                            "PropertyType": input_dictionary['PropertyType'], "Availability": input_dictionary['Availability'],
                            "PriceRange": input_dictionary['PriceRange'], "Amenities": input_dictionary['Amenities'],
                            "Description": input_dictionary['Description']}
        targeted_audience = input_dictionary['TargetedAudience']

        logging.info("Extracted property details from input dictionary")
        
        promotion = get_promotion(property_details, targeted_audience)
        logging.info("Generated promotion based on property details and targeted audience")


        return promotion

    except AttributeError as e:
        logging.error(f"Attribute error: {e}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        raise
    except KeyError as e:
        logging.error(f"Key error: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise
