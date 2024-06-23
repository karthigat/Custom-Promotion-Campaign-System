import requests
import json

url = "https://fe44-2401-4900-1cd1-bfa6-3816-9305-5d68-a928.ngrok-free.app/property"

input_property_details = {
                    "Name": "Urban Oasis Lofts",
                    "Location": "San Francisco, CA",
                    "PropertyType": "Loft Apartments",
                    "Availability": "2 Bed, 2 Bath | 3 Bed, 3 Bath | 4 Bed, 4 Bath",
                    "PriceRange": "$900K - $3M",
                    "Amenities": "[Private Beach Access,Infinity Pools,Spa and Wellness Center,Gourmet Kitchens with High-End Appliances,Secured Private Parking]",
                    "Description": "Located in the vibrant heart of San Francisco, Urban Oasis Lofts offer chic urban living with a touch of sophistication. These new-age lofts feature open floor plans, high ceilings, and large windows that flood the space with natural light. Residents enjoy unparalleled access to cultural landmarks, dining, and entertainment.",
                    "TargetedAudience": "young couple"
                    }

input_json = json.dumps(input_property_details)

# Send a POST request to the specified URL with the JSON data
response = requests.post(url, data=input_json)

print(response.text)