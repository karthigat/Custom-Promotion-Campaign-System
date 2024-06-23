from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from pyngrok import ngrok
from fastapi.middleware.cors import CORSMiddleware
import json
import nest_asyncio
from Custom_promotion.custom_promotion import get_promotion

app = FastAPI()

# @app.get("/")
# def hello_world():
#     return {"hellow":"world"}

# @app.get("/abc")
# def hello_world():
#     return {"hellow":"world"}

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def hello_world():
    return {"hellow":"world"}


@app.post('/property')
def prop_detail(input_parameters: model_input):
    
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    
    property_details = {"Name": input_dictionary['Name'], "Location": input_dictionary['Location'],
                        "PropertyType": input_dictionary['PropertyType'], "Availability": input_dictionary['Availability'],
                        "PriceRange": input_dictionary['PriceRange'], "Amenities": input_dictionary['Amenities'],
                        "Description": input_dictionary['Description']}
    targeted_audience = input_dictionary['TargetedAudience']

  
    promotion = get_promotion(property_details, targeted_audience)
    
    return {"test":test_test, "test1":test1_test}

# ngrok_tunnel = ngrok.connect(8000)
# print('Public URL:', ngrok_tunnel.public_url)
# nest_asyncio.apply()
# uvicorn.run(app, port=8000)
