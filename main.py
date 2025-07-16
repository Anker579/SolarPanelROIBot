import os
import googleapiclient.discovery
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get your API key from the environment variable
api_key = os.getenv("GOOGLE_API_KEY")

# Check if the API key is available
if not api_key:
    raise ValueError("API key not found. Make sure you have a .env file with GOOGLE_API_KEY set.")

# The service and version of the API
api_service_name = "solar"
api_version = "v1"

# The location for which to get solar data
# Replace with the desired latitude and longitude
latitude = 34.0522
longitude = -118.2437

def get_solar_data(lat, lon):
    """
    Calls the Google Solar API to get building insights for a given location.
    """
    try:
        # Build the service object
        service = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=api_key
        )

        # The specific API call for building insights
        request = service.buildingInsights().findClosest(
            location_latitude=lat, location_longitude=lon
        )

        # Execute the request
        response = request.execute()

        # Print the response
        print(response)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_solar_data(latitude, longitude)