# BIST MLOps Projesi

Bu proje, **Borsa Istanbul (BIST)** hisselerinin 3 aylik getiri tahminlerini yapmayi, tahmin sonuçlarini bir veri tabanina kaydetmeyi ve modeli izlemek için MLOps araçlari kullanmayi amaçlamaktadir. Proje, modern yazilim gelistirme ve veri bilimi prensiplerine dayali olarak insa edilmistir.

---

## ?? Proje Yapisi

```plaintext
BIST_MLops/
+-- data/
¦   +-- bist_tum_hisseler_temizlenmis.csv  # Veri seti
+-- models/
¦   +-- model_training.pkl                # Egitimli model dosyasi
+-- scripts/
¦   +-- api.py                            # FastAPI uygulamasi
¦   +-- drift_detection.py                # Model ve veri sapma tespiti
¦   +-- mysql_writer.py                   # MySQL baglantisi ve tahmin kaydi
¦   +-- mlflow_logger.py                  # MLflow entegrasyonu
+-- logs/
¦   +-- drift_detection.log               # Sapma tespiti log dosyasi
+-- Dockerfile                            # Docker yapilandirmasi
+-- Jenkinsfile                           # CI/CD pipeline yapilandirmasi
+-- requirements.txt                      # Proje bagimliliklari
+-- README.md                             # Proje dökümantasyonu
```

---

## ?? Nasil Çalistirilir?

### 1. Gerekli Ortam Kurulumu

#### a. Bagimliliklari Kurun
```bash
pip install -r requirements.txt
```

#### b. Docker Imajini Olusturun
```bash
docker build -t bist_mlops_api:latest .
```

#### c. Konteyneri Çalistirin
```bash
docker run -d --name bist_mlops_api_container -p 8010:8010 bist_mlops_api:latest
```

---

### 2. API'yi Çalistirma
FastAPI uygulamasi, `/predict` endpoint'ini kullanarak tahmin yapar.

#### Örnek Istek:
```bash
curl -X GET "http://localhost:8010/predict?stock_name=AGROT.IS"
```

#### Dönen Örnek Yanit:
```json
{
  "stock": "AGROT.IS",
  "name": "AG Anadolu Grubu Holding",
  "prediction": "12.34%",
  "message": "Tahmin basariyla yapildi ve kaydedildi."
}
```

---

## ?? Öne Çikan Özellikler

### ?? Model Egitim
- **Model**: Random Forest Regressor
- **Hedef Degisken**: 3 aylik getiri orani (%).
- **Özellikler**:
  - Fiyat/Kazanç Orani
  - PDDD Orani
  - Fiyat/Satis Orani
  - Volatilite
  - Piyasa Degeri
  - Son Fiyat

---

### ?? Drift Detection (Sapma Tespiti)
`drift_detection.py` ile:
- **Feature Drift**: Wasserstein mesafesi ile hesaplanir.
- **Model Drift**: Egitim ve yeni verinin tahmin hatalari arasindaki fark hesaplanir (MSE).

Sonuçlar `logs/drift_detection.log` dosyasina kaydedilir.

---

### ??? Tahminlerin Kaydi
- Tahmin sonuçlari **MySQL veri tabanina** kaydedilir.
- **Tablo Yapisi**:
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

### ?? MLflow Entegrasyonu
- Tahmin sonuçlari MLflow üzerinde loglanir.
- **Özellikler**:
  - Hisse adi (parametre olarak)
  - Tahmin sonucu (metrik olarak)

---

## ??? CI/CD Pipeline
### Jenkins Pipeline
1. Repository klonlanir.
2. Docker imaji olusturulur ve çalistirilir.
3. **MySQL** ve **MLflow** kontrol edilir.
4. API istekleri test edilir ve sonuçlar dogrulanir.

---

## ?? Gelistirme ve Iyilestirme Önerileri
- **Daha Fazla Test**: Uç senaryolari kapsayan testler eklenebilir.
- **Loglama**: Yapilandirilmis loglama mekanizmalari güçlendirilebilir.
- **Dokümantasyon**: API ve model kullanimi için daha fazla örnek eklenebilir.

---

## ????? Katkida Bulunma
Proje gelistirmelerine katkida bulunmak isterseniz, lütfen bir **Pull Request** olusturun veya [issue açin](#).
