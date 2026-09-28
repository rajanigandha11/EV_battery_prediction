from django import forms

CAR_MODEL_CHOICES = [
    ('Model S', 'Model S'),
    ('Model 3', 'Model 3'),
    ('Model X', 'Model X'),
    ('Model Y', 'Model Y'),
    ('Nissan Leaf', 'Nissan Leaf'),
    ('Chevy Bolt', 'Chevy Bolt'),
    ('Hyundai Kona', 'Hyundai Kona'),
    ('Other', 'Other'),
]

DRIVING_STYLE_CHOICES = [
    ('Aggressive', 'Aggressive'),
    ('Moderate', 'Moderate'),
    ('Eco', 'Eco'),
]

BATTERY_TYPE_CHOICES = [
    ('NMC', 'NMC'),
    ('LFP', 'LFP'),
    ('NCA', 'NCA'),
]

class BatteryPredictForm(forms.Form):
    car_model = forms.ChoiceField(choices=CAR_MODEL_CHOICES, label="Car Model", initial="Model 3")
    battery_capacity = forms.FloatField(label="Battery Capacity (kWh)", initial=75.0)
    vehicle_age_months = forms.FloatField(label="Vehicle Age (Months)", initial=24.0)
    total_cycles = forms.FloatField(label="Total Charging Cycles", initial=300.0)
    avg_temperature = forms.FloatField(label="Avg Temperature (°C)", initial=25.0)
    fast_charge_ratio = forms.FloatField(label="Fast Charge Ratio (0-1)", initial=0.3)
    avg_discharge_rate = forms.FloatField(label="Avg Discharge Rate (C)", initial=1.2)
    driving_style = forms.ChoiceField(choices=DRIVING_STYLE_CHOICES, label="Driving Style", initial="Moderate")
    internal_resistance = forms.FloatField(label="Internal Resistance (Ohm)", initial=0.05)
    battery_type = forms.ChoiceField(choices=BATTERY_TYPE_CHOICES, label="Battery Type", initial="NMC")
