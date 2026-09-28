import os
import pandas as pd

def run_spark_pipeline():
    try:
        from pyspark.sql import SparkSession
        from pyspark.sql import functions as F

        spark = SparkSession.builder \
            .appName("EV_Battery_ETL_Parquet") \
            .config("spark.driver.memory", "2g") \
            .config("spark.sql.parquet.compression.codec", "snappy") \
            .getOrCreate()

        spark.sparkContext.setLogLevel("WARN")

        # Ingest direct from source
        raw_df = spark.read.csv("data/ev_battery_degradation.csv", header=True, inferSchema=True)

        # Feature Engineering (Arrhenius thermal kinetics & cycle degradation ratios)
        enriched_df = raw_df \
            .withColumn("Thermal_Stress_Index", F.round(F.col("Avg_Temperature_C") * F.col("Fast_Charge_Ratio"), 4)) \
            .withColumn("Cycles_Per_Month", F.round(F.col("Total_Charging_Cycles") / (F.col("Vehicle_Age_Months") + 1e-5), 4)) \
            .withColumn("Resistance_Per_Cycle", F.round(F.col("Internal_Resistance_Ohm") / (F.col("Total_Charging_Cycles") + 1e-5), 6))

        enriched_df.write \
            .mode("overwrite") \
            .partitionBy("Battery_Type") \
            .parquet("data/processed_parquet")

        print("PySpark ETL complete: Data processed and partitioned into Parquet format successfully.")
        spark.stop()
    except Exception as e:
        print(f"PySpark write notice: {e}")
        print("Executing Pandas/PyArrow feature engineering & parquet generation...")

        df = pd.read_csv("data/ev_battery_degradation.csv")
        df['Thermal_Stress_Index'] = (df['Avg_Temperature_C'] * df['Fast_Charge_Ratio']).round(4)
        df['Cycles_Per_Month'] = (df['Total_Charging_Cycles'] / (df['Vehicle_Age_Months'] + 1e-5)).round(4)
        df['Resistance_Per_Cycle'] = (df['Internal_Resistance_Ohm'] / (df['Total_Charging_Cycles'] + 1e-5)).round(6)

        os.makedirs("data/processed_parquet", exist_ok=True)
        df.to_parquet("data/processed_parquet", partition_cols=["Battery_Type"], index=False)
        print("Data processed and partitioned into Parquet format successfully via Pandas/PyArrow.")

if __name__ == "__main__":
    run_spark_pipeline()