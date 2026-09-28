from django.shortcuts import render
import os
import joblib
import pandas as pd
from django.shortcuts import render
from .forms import BatteryPredictForm

from django.conf import settings
MODEL_PATH = os.path.join(settings.BASE_DIR, "artifacts", "xgb_soh_model.pkl")
pipeline = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

def index(request):
    return render(request, "battery_app/index.html")

def predict_view(request):
    prediction = None
    status = None
    badge_class = "success"

    if request.method == "POST":
        form = BatteryPredictForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Reconstruct engineered features
            temp = data['avg_temperature']
            fc_ratio = data['fast_charge_ratio']
            cycles = data['total_cycles']
            age = data['vehicle_age_months']
            ir = data['internal_resistance']

            thermal_stress = temp * fc_ratio
            cycles_per_month = cycles / (age + 1e-5)
            res_per_cycle = ir / (cycles + 1e-5)

            input_df = pd.DataFrame([{
                'Car_Model': data['car_model'],
                'Battery_Capacity_kWh': data['battery_capacity'],
                'Vehicle_Age_Months': age,
                'Total_Charging_Cycles': cycles,
                'Avg_Temperature_C': temp,
                'Fast_Charge_Ratio': fc_ratio,
                'Avg_Discharge_Rate_C': data['avg_discharge_rate'],
                'Driving_Style': data['driving_style'],
                'Internal_Resistance_Ohm': ir,
                'Thermal_Stress_Index': round(thermal_stress, 4),
                'Cycles_Per_Month': round(cycles_per_month, 4),
                'Resistance_Per_Cycle': round(res_per_cycle, 6),
                'Battery_Type': data['battery_type']
            }])

            if pipeline:
                predicted_soh = float(pipeline.predict(input_df)[0])
                prediction = round(predicted_soh, 2)
                if prediction >= 80.0:
                    status = "Healthy"
                    badge_class = "success"
                else:
                    status = "Replace Required"
                    badge_class = "danger"
    else:
        form = BatteryPredictForm()

    return render(request, "battery_app/predict.html", {
        "form": form,
        "prediction": prediction,
        "status": status,
        "badge_class": badge_class
    })


