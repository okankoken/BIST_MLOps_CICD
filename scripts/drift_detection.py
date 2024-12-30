import pandas as pd
import numpy as np
from scipy.stats import wasserstein_distance
from sklearn.metrics import mean_squared_error
import joblib

# Drift detection icin log dosyasi
log_file = "/home/train/mlops4/BIST_MLops/logs/drift_detection.log"

# Drift kontrolu fonksiyonlari
def detect_feature_drift(train_data, new_data):
    """Her feature icin Wasserstein mesafesi hesaplar."""
    drift_results = {}
    for column in train_data.columns:
        if train_data[column].dtype in [np.float64, np.int64]:
            drift_results[column] = wasserstein_distance(train_data[column], new_data[column])
    return drift_results

def detect_model_drift(y_true, y_pred_train, y_pred_new):
    """Model drift icin MSE farkini hesaplar."""
    mse_train = mean_squared_error(y_true, y_pred_train)
    mse_new = mean_squared_error(y_true, y_pred_new)
    drift_value = abs(mse_new - mse_train)
    return drift_value

# Veriyi yukle
train_data_path = "/home/train/mlops4/BIST_MLops/data/bist_tum_hisseler_temizlenmis.csv"
train_data = pd.read_csv(train_data_path)

# Modeli yukle
model_path = "/home/train/mlops4/BIST_MLops/models/model_training.pkl"
model = joblib.load(model_path)

# Modelde kullanilan ozellikler
selected_features = [
    "FiyatKazanc Orani", "PDDD Orani", "FiyatSatis Orani", 
    "Volatilite", "Piyasa Degeri", "Son Fiyat"
]
target_column = "3 Ay Degisim (%)"

# Yeni veri simulasyonu (Gercek API verisiyle degistirilebilir)
new_data = train_data.sample(frac=0.1, random_state=42)

# Drift Detection
feature_drift = detect_feature_drift(train_data[selected_features], new_data[selected_features])

# Model drift icin y_true ve y_pred hazirligi
y_true_new = new_data[target_column]  # Yeni veriye uygun hedef degisken
y_pred_train = model.predict(train_data[selected_features])
y_pred_new = model.predict(new_data[selected_features])

model_drift = detect_model_drift(
    y_true_new,  # Yeni veriye uygun y_true
    y_pred_train[:len(y_true_new)],  # Train tahminlerini yeni veriyle esit uzunlukta tut
    y_pred_new
)

# Log dosyasina yaz
with open(log_file, "a") as log:
    log.write("Feature Drift:\n")
    for feature, drift_value in feature_drift.items():
        log.write(f"{feature}: {drift_value:.4f}\n")
    log.write(f"Model Drift: {model_drift:.4f}\n")
    log.write("Drift detection completed.\n\n")

print("Drift detection tamamlandi. Sonuclar log dosyasina yazildi.")
