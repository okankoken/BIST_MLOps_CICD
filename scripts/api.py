from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd

# FastAPI uygulamasi
app = FastAPI()

# Model ve veri yollari
model_path = "./models/model_training.pkl"
data_path = "./data/bist_tum_hisseler_temizlenmis.csv"

# Model ve veri setini yukleme
model = joblib.load(model_path)
df = pd.read_csv(data_path)

# Modelde kullanilan ozellikler
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
        raise HTTPException(status_code=404, detail="Hisse senedi bulunamadi")

    # Modelde kullanilan bagimsiz degiskenleri secme
    input_data = stock_data[selected_features].fillna(0)

    # Tahmin yapma
    prediction = model.predict(input_data)[0]

    # Hisse Adi'ni ekleme
    stock_name_full = stock_data["Adi"].iloc[0]

    return {
        "stock": stock_name,
        "name": stock_name_full,
        "prediction": f"{prediction:.2f}%",
        "message": "3 aylik tahmin yuzdesi hesaplandi"
    }
