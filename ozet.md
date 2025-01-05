# Proje Özeti

Bu dosya, BIST MLOps projesi için yapılan ve yapılacak işleri özetlemektedir. Projenin amacı, Borsa İstanbul (BIST) hisse senetlerinin 3 aylık getiri tahminlerini yapmak, bu tahminleri bir veri tabanına kaydetmek ve modeli izlemek için MLOps araçlarını kullanmaktır.

---

## 📝 Yapılanlar ve Hedefler

Proje, aşağıdaki adımlarla yapılandırılmıştır:

---

### 📊 1. Veri Seti
- **Veri Kaynağı**: [BIST Veri Seti](https://github.com/okankoken/BIST_MLOps/blob/main/data/bist_tum_hisseler_temizlenmis.csv)  
- **Durum**: ✅ Yapıldı  
- Veri seti indirildi ve model eğitimi için temizlendi.

---

### 🤖 2. Modelleme
- **Makine Öğrenmesi Modeli**:
  - 3 aylık süreçte en fazla getiri sağlayan hisse senetlerini analiz etmek için model oluşturuldu.
  - **ML Pipeline** kullanıldı.  
  - **Durum**: ✅ Yapıldı  
- **Not**: Bağımsız değişkenler ve finans literatürü baz alınarak özellik seçimi yapıldı.

---

### 🌐 3. Deployment
- **API Geliştirme**:
  - **3 aylık tahminler için bir API** geliştirildi.
  - **FastAPI** kullanılarak tahmin sonuçları döndürüldü.
  - **Durum**: ✅ Yapıldı  
- **Path/Query Parameter**:
  - 3 aylık tahminler için path veya query parametreleri kullanıldı.
  - **Durum**: ✅ Yapıldı  
- **Drift Detection**:
  - **Veri/Model Drift Tespiti** için mekanizma (drift_detection.py) oluşturuldu.  
  - **Durum**: ✅ Yapıldı  
  - **Not**: Mekanizma, verideki veya model performansındaki sapmaları tespit eder.
- **CI/CD Pipeline**:
  - **Jenkins/Gitea** kullanılarak model dağıtımı otomasyonu sağlandı.
  - **Durum**: ✅ Yapıldı  
- **MLflow Entegrasyonu**:
  - Model parametreleri ve performans metrikleri MLflow üzerinde loglandı.
  - **Durum**: ✅ Yapıldı  

---

### ⚙️ 4. Altyapı (Infrastructure)
- **Docker**:
  - Altyapı olarak Docker container kullanıldı.
  - **Durum**: ✅ Yapıldı  
- **Veritabanı**:
  - **MySQL** kullanıldı ve tahmin sonuçları veri tabanına yazıldı.
  - **Durum**: ✅ Yapıldı  

---

## 🚀 Notlar
- **Hedef**: Drift tespit mekanizmasını daha iyi anlamak ve kullanmak.
- **Eksik Kalan İşler**: Projenin dokümantasyonu genişletilebilir, test senaryoları artırılabilir.
