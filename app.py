import streamlit as st
import os
from data import geocoder, solardatafetcher
from dotenv import load_dotenv

# Load and check API from env variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Make sure you have a .env file with GOOGLE_API_KEY set.")

st.set_page_config(
    page_title = "Solar Panel ROI Calculator"
    page_icon="☀️",
    )

st.title("Welcome to the Solar Panel Return on Investment Calculator")
st.write("This simple data app figures out the energy production of a given solar panel in your location, then uses the current energy price cap to compute your savings and from that the return on investment of the panels.")
