CREATE DATABASE IF NOT EXISTS ev_analytics_db;
USE ev_analytics_db;

CREATE EXTERNAL TABLE IF NOT EXISTS ev_battery_health_gold (
    Vehicle_ID STRING,
    Car_Model STRING,
    Battery_Capacity_kWh DOUBLE,
    Vehicle_Age_Months INT,
    Total_Charging_Cycles INT,
    Avg_Temperature_C DOUBLE,
    Fast_Charge_Ratio DOUBLE,
    Avg_Discharge_Rate_C DOUBLE,
    Driving_Style STRING,
    Internal_Resistance_Ohm DOUBLE,
    SoH_Percent DOUBLE,
    Battery_Status STRING,
    Thermal_Stress_Index DOUBLE,
    Cycles_Per_Month DOUBLE,
    Resistance_Per_Cycle DOUBLE
)
PARTITIONED BY (Battery_Type STRING)
STORED AS PARQUET
LOCATION '/data/ev_battery/gold_parquet';

-- Recover partitions
MSCK REPAIR TABLE ev_battery_health_gold;

-- Fleet analytical query
SELECT 
    Battery_Type,
    Car_Model,
    COUNT(*) AS total_fleet,
    ROUND(AVG(SoH_Percent), 2) AS avg_soh,
    ROUND(AVG(Thermal_Stress_Index), 2) AS avg_thermal_stress
FROM ev_battery_health_gold
GROUP BY Battery_Type, Car_Model;