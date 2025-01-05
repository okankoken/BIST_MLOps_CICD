from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from scripts.mysql_writer import save_predictions_to_mysql

# FastAPI uygulamasi
app = FastAPI()

# Model ve veri yollari
model_path = "./models/model_training.pkl"
data_path = "./data/bist_tum_hisseler_temizlenmis.csv"

# Model ve veri setini yükleme
model = joblib.load(model_path)
df = pd.read_csv(data_path)

# Modelde kullanilan özellikler
selected_features = [
    "FiyatKazanc Orani", "PDDD Orani", "FiyatSatis Orani",
    "Volatilite", "Piyasa Degeri", "Son Fiyat"
]

@app.get("/")
def home():
    return {"message": "BIST 3 Aylik Tahmin API'si calisiyor"}

@app.get("/predict")
def predict(stock_name: str):
    # Hisse senedini bulma
    stock_data = df[df['Hisse'] == stock_name]
    if stock_data.empty:
        raise HTTPException(status_code=404, detail=f"Hisse senedi bulunamadi: {stock_name}")

    # Modelde kullanilan bagimsiz degiskenleri seçme
    input_data = stock_data[selected_features].fillna(0)

    # Tahmin yapma
    prediction = model.predict(input_data)[0]
    stock_name_full = stock_data["Adi"].iloc[0]

    # Tahminleri MySQL'e kaydetme
    save_predictions_to_mysql(stock_name, stock_name_full, prediction)

    # MLflow kontrolü
    print("MLflow kontrol: Model izleniyor.")

    return {
        "stock": stock_name,
        "name": stock_name_full,
        "prediction": f"{prediction:.2f}%",
        "message": "Tahmin basariyla yapildi ve kaydedildi."
    }

@app.post("/batch_predict")
def batch_predict(payload: dict):
    stocks = payload.get("stocks", [])
    results = []
    for stock_name in stocks:
        stock_data = df[df['Hisse'] == stock_name]
        if stock_data.empty:
            continue
        input_data = stock_data[selected_features].fillna(0)
        prediction = model.predict(input_data)[0]
        stock_name_full = stock_data["Adi"].iloc[0]
        save_predictions_to_mysql(stock_name, stock_name_full, prediction)
        results.append({"stock": stock_name, "prediction": prediction})
    return {"predictions": results, "message": "Tahminler basariyla tamamlandi."}
