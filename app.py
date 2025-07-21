import streamlit as st
from streamlit_folium import st_folium
import folium
import os
from data.geocoder import Geocoder
from data.solardatafetcher import Solardatafetcher
from data.calculator import Calculator
from dotenv import load_dotenv

# Load and check API from env variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Make sure you have a .env file with GOOGLE_API_KEY set.")

my_fetcher = Solardatafetcher()
my_geocoder = Geocoder()
my_calculator = Calculator()

st.set_page_config(layout="wide")
st.set_page_config(
    page_title = "UK Solar Panel ROI Calculator",
    page_icon="☀️",
    )

if "latlong" not in st.session_state:
    st.session_state.latlong = None

st.title("Welcome to the UK Solar Panel Return on Investment Calculator")
st.write("This simple data app figures out the energy production of a given solar panel in your location, then uses the current energy price cap to compute your savings and from that the return on investment of the panels.")
st.write("The first thing we'll need, where in the UK do you live?")

map_col, address_col = st.columns(2)

with map_col:
    DEFAULT_LATITUDE = 52.5
    DEFAULT_LONGITUDE = -1.9
    
    # Initialize session state variables if they don't exist
    if "selected_latitude" not in st.session_state:
        st.session_state.selected_latitude = None
    if "selected_longitude" not in st.session_state:
        st.session_state.selected_longitude = None
    

    zoom_level = 7
    map_center = [DEFAULT_LATITUDE, DEFAULT_LONGITUDE]


    m = folium.Map(location=map_center, zoom_start=zoom_level)

    m.add_child(folium.LatLngPopup())

    f_map = st_folium(m, width=725)

    # This block captures a map click and stores the data
    if f_map.get("last_clicked"):
        st.session_state.selected_latitude = f_map["last_clicked"]["lat"]
        st.session_state.selected_longitude = f_map["last_clicked"]["lng"]
        st.session_state.latlong = [st.session_state.selected_latitude, st.session_state.selected_longitude]

    # This block displays the stored coordinates from a click
    if st.session_state.selected_latitude and st.session_state.selected_longitude:
        st.success(f"Stored position: {round(st.session_state.selected_latitude, 4)}, {round(st.session_state.selected_longitude, 4)}")

 
with address_col:
    st.write("Or alternatively, enter your address here")

    with st.form(key="address_form"):
        col1, col2 = st.columns(2)
        h_number = col1.text_input("House Number")
        r_name = col2.text_input("Road Name")
        
        col3, col4 = st.columns(2)
        town = col3.text_input("Town/City")
        postcode = col4.text_input("Postcode")
        
        submit_address = st.form_submit_button("Submit Address")

    if submit_address:
        address_elements = [h_number, r_name, town, postcode]
        # 1. Store the geocoded result in session_state
        st.session_state.latlong = my_geocoder.get_latlong(address=address_elements)

    if st.session_state.latlong:
        st.write("#### Your latitude and longitude is:")
        st.write(f"#### {round(st.session_state.latlong[0],4)},{round(st.session_state.latlong[1],4)}")

st.write("Tell us some details about the Solar System you will be installing and your home")

tech_options = {
    "Crystalline Silicon: Mono and Polycrystalline": "crystSi",
    "CIS: Copper Indium Selenide": "CIS",
    "CdTe: Cadmium Telluride": "CdTe",
    "Unknown/Other": "Unknown"
}

cola, colb, colc = st.columns(3)
cold, cole = st.columns(2)

details = {}
details["peakpower"] = cola.number_input("Solar System Peak Power in kWh")
user_tech_choice = colb.selectbox(
    label="Select what type of Solar Panel you will be using",
    options=list(tech_options.keys()),
    )
details["system_cost"] = colc.number_input("How much will the Solar Panels & Installation cost in £")
details["energy_cost"] = 10e-3 * cold.number_input("How much do you pay for electricity in pence per kWh")
details["usage"] = cole.number_input("What is your average monthly energy usage across the year? (kWh)")

details["pv_technology"] = tech_options[user_tech_choice]

#info labels
cola.markdown(body="Peak Power", help="The 'Peak Power' is how many kWh your whole system will produce e.g. if your system has 10 400W Panels, the peak power is 4kW.")
colb.markdown(body="Solar Panel Technology", help="This essentially refers to the materials used for the panels, this information will be provided by the supplier.")

cold.markdown(body="I Don't Know", help="If you're not sure what you pay for electricity, enter 0 and the current OFGEM energy price cap will be used.")
cole.markdown(body="I Don't Know", help="If you're not sure, once again enter 0 and we will use the average for a UK household")

if st.session_state.latlong == None:
    location = [st.session_state.selected_latitude, st.session_state.selected_longitude]
else:
    location = st.session_state.latlong

calculate = st.button(label="Calculate my ROI!")


if calculate:
    if st.session_state.latlong is None:
        st.error("Please select a location on the map or enter an address to continue")
    elif my_geocoder.check_is_UK(location=location):
        production = my_fetcher.PVGIS_request(location=location, sp_details=details)
        #st.write(production)
        #st.write(production["month_average"])
        #st.write(details["energy_cost"])

        monthly_saving, export_profit, months_to_ROI, years_to_ROI = my_calculator.calculate_ROI(system_details=details, production=production)

        st.write(export_profit)

        st.write(f"You will be saving £{monthly_saving} per month")
        st.write(f"Additionally, you will be making £{export_profit} per month from exporting excess energy to the grid")

        st.write(f"That means it will take {months_to_ROI} months or {years_to_ROI} years to break even from your initial investment of £{details['system_cost']}")
    else:
        st.error("The location you have entered does not appear to be in the UK, please check your address or lap location")