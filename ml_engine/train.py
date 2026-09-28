import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, root_mean_squared_error
import xgboost as xgb

def train():
    os.makedirs("artifacts", exist_ok=True)
    df = pd.read_parquet("data/processed_parquet")

    X = df.drop(columns=["Vehicle_ID", "SoH_Percent", "Battery_Status"])
    y = df["SoH_Percent"]

    categorical_cols = ["Car_Model", "Driving_Style", "Battery_Type"]
    numerical_cols = [c for c in X.columns if c not in categorical_cols]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", numerical_cols),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical_cols)
        ]
    )

    model = xgb.XGBRegressor(
        n_estimators=250,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", model)])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    print(f"Model Performance:")
    print(f"R^2 Score: {r2_score(y_test, preds):.4f}")
    print(f"RMSE:      {root_mean_squared_error(y_test, preds):.4f}")
    print(f"MAE:       {mean_absolute_error(y_test, preds):.4f}")

    joblib.dump(pipeline, "artifacts/xgb_soh_model.pkl")
    print("Model saved to artifacts/xgb_soh_model.pkl")

if __name__ == "__main__":
    train()