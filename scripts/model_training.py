import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# Veri yukleme
file_path = "/home/train/mlops4/BIST_MLops/data/bist_tum_hisseler_temizlenmis.csv"
df = pd.read_csv(file_path)

# Hedef degisken ve secilen bagimsiz degiskenler
target_column = "3 Ay Degisim (%)"

# Finansal olarak anlamli bagimsiz degiskenler
selected_features = [
    "FiyatKazanc Orani", "PDDD Orani", "FiyatSatis Orani", 
    "Volatilite", "Piyasa Degeri", "Son Fiyat"
]

# Bagimli ve bagimsiz degiskenler
X = df[selected_features]
y = df[target_column]

# Eksik degerleri doldurma (numerik ortalamalar ile)
X.fillna(X.mean(), inplace=True)

# Veriyi bolme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model egitimi ve hiperparametre optimizasyonu
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# En iyi model
best_model = grid_search.best_estimator_

# Tahmin ve performans metrikleri
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"R^2 Score: {r2:.4f}")

# Ozellik onem siralamasi
feature_importances = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": best_model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("Feature Importances:")
print(feature_importances)

# Modeli kaydetme
model_path = "/home/train/mlops4/BIST_MLops/models/model_training.pkl"
joblib.dump(best_model, model_path)

print(f"Model basariyla kaydedildi: {model_path}")