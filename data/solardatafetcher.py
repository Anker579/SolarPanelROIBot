import requests
import os
from dotenv import load_dotenv


#load_dotenv()

class solardatafetcher():
    def __init__(self):
        pass

    def PVGIS_request(self, location, sp_details):
        #location is a list of latitude then longitude
        #sp_details is a dictionary containing the database, peak power, system loss and pv technology
        latitude = location[0]
        longitude = location[1]
        system_loss = 14

        database = "PVGIS-SARAH3"
        peak_power = sp_details["peakpower"]
        #system_loss = sp_details["system_loss"]
        pv_technology = sp_details["pv_technology"] # should be one of crystSi, CIS, CdTe or Unknown

        power_url = f"https://re.jrc.ec.europa.eu/api/v5_3/PVcalc?lat={latitude}&lon={longitude}&pvtechchoice={pv_technology}&raddatabase={database}&peakpower={peak_power}&loss={system_loss}&outputformat=json"

        response = requests.get(power_url).json()
        monthly_production = []

        for x in response["outputs"]["monthly"]["fixed"]:
            monthly_production.append(x["E_m"])
        
        year_average = response["outputs"]["totals"]["fixed"]["E_y"]
        month_average = response["outputs"]["totals"]["fixed"]["E_m"]#average per month across the year
        
        #all in kWh
        production = {"year": year_average, "per_month":monthly_production, "month_average":month_average}
        return production


