import requests
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("API key not found. Make sure you have a .env file with GOOGLE_API_KEY set.")

class geocoder():
    def __init__(self):
        pass

    def address_parser(self, inputted_address):
        #input address should be a string of parts
        formatted_address_elements = []
        for address_element in inputted_address:
            new_element = address_element.replace(" ", "+")
            formatted_address_elements.append(new_element)
        parsed_address = ",".join(formatted_address_elements)
        return parsed_address
    
    def get_latlong(self, address):
        formatted_address = self.address_parser(inputted_address=address)
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={formatted_address}&key={GOOGLE_API_KEY}"
        try:
            response = requests.get(url).json()
            latlong_dict = response["results"][0]["geometry"]["location"]
            latitude = latlong_dict["lat"]
            longitude = latlong_dict["lng"]
            return [latitude, longitude]
        except response.status_code != 200:
            pass

