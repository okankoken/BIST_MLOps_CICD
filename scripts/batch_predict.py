import requests

# Hisse isimlerini dosyadan yukle
with open("/home/train/mlops4/BIST_MLops/data/bist_symbols_with_IS.txt", "r") as file:
    stocks = [line.strip() for line in file.readlines()]

# API'ye POST istegi gonder
response = requests.post(
    "http://localhost:8010/batch_predict",
    json=stocks  # Liste olarak gonderiyoruz
)

# Sonuclari yazdir
print(response.json())
