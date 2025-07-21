

class Calculator():
    def __init__(self):
        pass

    def calculate_ROI(self, system_details, production):
        system_details["usage"] = production["month_average"] * 0.26

        if system_details["usage"] <= production["month_average"]:
            monthly_saving = system_details["usage"] * system_details["energy_cost"]
        elif system_details["usage"] >= production["month_average"]:
            monthly_saving = system_details["energy_cost"] * production["month_average"]
        
        export_price = 0.12  # export price per kWh
        export_profit = round((production["month_average"] - system_details["usage"]) * export_price if production["month_average"] > system_details["usage"] else 0, 2)

        months_to_ROI = round(system_details["system_cost"] / (monthly_saving + export_profit), 2)
        years_to_ROI = round(months_to_ROI/12, 2)

        return [monthly_saving, export_profit, months_to_ROI, years_to_ROI]