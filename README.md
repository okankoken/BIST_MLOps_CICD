# BIST MLOps Projesi

Bu proje, **Borsa İstanbul (BIST)** hisselerinin 3 aylık getiri tahminlerini yapmayı, tahmin sonuçlarını bir veri tabanına kaydetmeyi ve modeli izlemek için MLOps araçları kullanmayı amaçlamaktadır. Proje, modern yazılım geliştirme ve veri bilimi prensiplerine dayalı olarak inşa edilmiştir.

---

## 📂 Proje Yapısı

```plaintext
BIST_MLops/
├── data/
│   └── bist_tum_hisseler_temizlenmis.csv  # Veri seti
├── models/
│   └── model_training.pkl                # Eğitimli model dosyası
├── scripts/
│   ├── api.py                            # FastAPI uygulaması
│   ├── drift_detection.py                # Model ve veri sapma tespiti
│   ├── mysql_writer.py                   # MySQL bağlantısı ve tahmin kaydı
│   └── mlflow_logger.py                  # MLflow entegrasyonu
├── logs/
│   └── drift_detection.log               # Sapma tespiti log dosyası
├── Dockerfile                            # Docker yapılandırması
├── Jenkinsfile                           # CI/CD pipeline yapılandırması
├── requirements.txt                      # Proje bağımlılıkları
└── README.md                             # Proje dökümantasyonu
```

---

## 🚀 Nasıl Çalıştırılır?

### 1. Gerekli Ortam Kurulumu

#### a. Bağımlılıkları Kurun
```bash
pip install -r requirements.txt
```

#### b. Docker İmajını Oluşturun
```bash
docker build -t bist_mlops_api:latest .
```

#### c. Konteyneri Çalıştırın
```bash
docker run -d --name bist_mlops_api_container -p 8010:8010 bist_mlops_api:latest
```

---

### 2. API'yi Çalıştırma
FastAPI uygulaması, `/predict` endpoint'ini kullanarak tahmin yapar.

#### Örnek İstek:
```bash
curl -X GET "http://localhost:8010/predict?stock_name=AGROT.IS"
```

#### Dönen Örnek Yanıt:
```json
{
  "stock": "AGROT.IS",
  "name": "AG Anadolu Grubu Holding",
  "prediction": "12.34%",
  "message": "Tahmin başarıyla yapıldı ve kaydedildi."
}
```

---

## 🔍 Öne Çıkan Özellikler

### 📊 Model Eğitim
- **Model**: Random Forest Regressor
- **Hedef Değişken**: 3 aylık getiri oranı (%).
- **Özellikler**:
  - Fiyat/Kazanç Oranı
  - PDDD Oranı
  - Fiyat/Satış Oranı
  - Volatilite
  - Piyasa Değeri
  - Son Fiyat

---

### 🔄 Drift Detection (Sapma Tespiti)
`drift_detection.py` ile:
- **Feature Drift**: Wasserstein mesafesi ile hesaplanır.
- **Model Drift**: Eğitim ve yeni verinin tahmin hataları arasındaki fark hesaplanır (MSE).

Sonuçlar `logs/drift_detection.log` dosyasına kaydedilir.

---

### 🗃️ Tahminlerin Kaydı
- Tahmin sonuçları **MySQL veri tabanına** kaydedilir.
- **Tablo Yapısı**:
  ```sql
  CREATE TABLE bist_predictions (
      id INT AUTO_INCREMENT PRIMARY KEY,
      stock_name VARCHAR(255) NOT NULL,
      stock_name_full VARCHAR(255) NOT NULL,
      prediction FLOAT NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```

---

### 📈 MLflow Entegrasyonu
- Tahmin sonuçları MLflow üzerinde loglanır.
- **Özellikler**:
  - Hisse adı (parametre olarak)
  - Tahmin sonucu (metrik olarak)

---

## 🛠️ CI/CD Pipeline
### Jenkins Pipeline
1. Repository klonlanır.
2. Docker imajı oluşturulur ve çalıştırılır.
3. **MySQL** ve **MLflow** kontrol edilir.
4. API istekleri test edilir ve sonuçlar doğrulanır.

---

## 🔧 Geliştirme ve İyileştirme Önerileri
- **Daha Fazla Test**: Uç senaryoları kapsayan testler eklenebilir.
- **Loglama**: Yapılandırılmış loglama mekanizmaları güçlendirilebilir.
- **Dokümantasyon**: API ve model kullanımı için daha fazla örnek eklenebilir.

---

## 👨‍💻 Katkıda Bulunma
Proje geliştirmelerine katkıda bulunmak isterseniz, lütfen bir **Pull Request** oluşturun veya [issue açın](#).
