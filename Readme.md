# BIST MLOps Projesi

Bu proje, **Borsa İstanbul (BIST)** hisselerinin 3 aylık getiri tahminlerini yapmayı, tahmin sonuçlarını bir veri tabanına kaydetmeyi ve modeli izlemek için MLOps araçları kullanmayı amaçlamaktadır. Proje, modern yazılım geliştirme ve veri bilimi prensiplerine dayalı olarak inşa edilmiştir.

---

## 🚀 Kullanılan Teknolojiler ve Araçlar

| Teknoloji/Araç   | Açıklama                                 | Logo                                                                                 |
|-------------------|------------------------------------------|--------------------------------------------------------------------------------------|
| **Yahoo Finance**| Hisse verilerinin kaynağı               | ![Yahoo Finance](https://upload.wikimedia.org/wikipedia/commons/8/8f/Yahoo%21_Finance_logo_2021.png) |
| **FastAPI**       | Python tabanlı web framework              | ![FastAPI](https://miro.medium.com/v2/resize:fit:1023/1*du7p50wS_fIsaC_lR18qsg.png)                        |
| **Uvicorn**       | FastAPI için ASGI sunucusu              | ![Uvicorn](https://www.uvicorn.org/uvicorn.png)                        |
| **MLflow**        | Model takibi ve metriklerin loglanması  | ![MLflow](https://miro.medium.com/v2/resize:fit:750/0*jYRVQGwW29Te4cPq.png)                   |
| **MySQL**         | Tahmin sonuçlarının veri tabanı         | ![MySQL](https://www.mysql.com/common/logos/logo-mysql-170x115.png)                 |
| **Docker**        | Uygulama konteynerlemesi               | ![Docker](https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png) |
| **Jenkins**       | CI/CD otomasyonu                       | ![Jenkins](https://www.jenkins.io/images/logos/jenkins/jenkins.svg)                 |

---

## 📂 Proje Yapısı

```plaintext
BIST_MLops/
├── data
│   ├── bist_symbols_with_IS.txt         # Hisse sembollerini içeren dosya
│   └── bist_tum_hisseler_temizlenmis.csv # Temizlenmiş hisse verileri
├── Dockerfile                            # Docker yapılandırması
├── Jenkinsfile                           # CI/CD pipeline tanımı
├── logs
│   └── drift_detection.log              # Drift tespit log dosyası
├── models
│   └── model_training.pkl               # Eğitimli model
├── ozet.md                               # Proje özet bilgileri
├── README.md                             # Proje dokümantasyonu
├── requirements.txt                      # Python bağımlılıkları
└── scripts
    ├── api.py                           # FastAPI uygulaması
    ├── batch_predict.py                 # Toplu tahmin script'i
    ├── drift_detection.py               # Drift tespiti için script
    ├── __init__.py                      # Modül tanımlama
    ├── mlflow_logger.py                 # MLflow entegrasyonu
    ├── model_training.py                # Model eğitim script'i
    ├── mysql_writer.py                  # MySQL bağlantı script'i
    └── __pycache__                      # Derlenmiş Python dosyaları
        ├── api.cpython-312.pyc
        ├── __init__.cpython-312.pyc
        ├── mlflow_logger.cpython-312.pyc
        └── mysql_writer.cpython-312.pyc
```

---

## 🚀 Kullanım Adımları

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

### 2. Veri Seti ve Model Eğitimi
- **Veri Seti**: `data/bist_tum_hisseler_temizlenmis.csv`
- **Model Eğitim Script'i**: `scripts/model_training.py`
- Model eğitimi için aşağıdaki komutu çalıştırın:

```bash
python scripts/model_training.py
```
Bu işlem, eğitilmiş modeli `models/model_training.pkl` dosyasına kaydeder ve MLflow üzerinde model bilgilerini loglar.

---

### 3. FastAPI Uygulaması
FastAPI uygulaması, `/predict` ve `/batch_predict` endpoint'leri üzerinden tahmin yapar.

- **Uygulamayı Başlatmak için**:

```bash
uvicorn scripts.api:app --reload --host 0.0.0.0 --port 8010
```

- **Tekil Tahmin İçin**:

```bash
curl -X GET "http://localhost:8010/predict?stock_name=AGROT.IS"
```

- **Toplu Tahmin İçin**:

`batch_predict.py` script'ini kullanın:

```bash
python scripts/batch_predict.py
```
Bu script, `data/bist_symbols_with_IS.txt` dosyasındaki hisse sembollerini API'ye gönderir ve sonuçları görüntüler.

---

### 4. Tahmin Sonuçlarının MySQL'de Kontrolü
- Tahminler, **`bist_predictions`** tablosuna kaydedilir.
- Tablodaki sonuçları kontrol etmek için:

```sql
SELECT * FROM bist_predictions ORDER BY prediction DESC;
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
- **Feature Drift**: Wasserstein mesafesi ile hesaplanır.
- **Model Drift**: Eğitim ve yeni verinin tahmin hataları arasındaki fark hesaplanır (MSE).

Sonuçlar `logs/drift_detection.log` dosyasına kaydedilir.

---

### 📈 MLflow Entegrasyonu
- MLflow, model eğitim sürecindeki parametreleri, performans metriklerini, model adını ve kullanılan veri setini takip eder.
- Loglanan bilgiler:
  - **Model İsmi**: Kullanılan modelin adı.
  - **Veri Seti**: Modelin eğitildiği veri setinin yolu.
  - **Parametreler**: Model hiperparametreleri (ör. `n_estimators`, `max_depth`).
  - **Metrikler**: Model performans metrikleri (ör. `MSE`, `MAE`, `R²`).
- MLflow UI'yi başlatmak için:

```bash
mlflow ui
```

Tarayıcınızdan http://localhost:5000 adresine giderek detayları görüntüleyebilirsiniz.

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

### 🛠️ CI/CD Pipeline
### Jenkins Pipeline
1. Repository klonlanır.
2. Docker imajı oluşturulur ve çalıştırılır.
3. **MySQL** ve **MLflow** kontrol edilir.
4. API istekleri test edilir ve sonuçlar doğrulanır.

---

### ⚠️ Önemli Uyarı: Yatırım Tavsiyesi Değildir!

Bu proje, yalnızca veri bilimi ve makine öğrenimi uygulamalarını göstermek amacıyla geliştirilmiştir. **Hiçbir şekilde yatırım tavsiyesi olarak değerlendirilmemelidir.** Hisse senetleri ve diğer finansal araçlarla ilgili kararlarınızı alırken bir finans uzmanına veya yetkili bir danışmana başvurmanız önerilir.
---
