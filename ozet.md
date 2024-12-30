tekrar özetliyorum:

yapılmayanları yapalım hadi : 

problem yaşamamam lazım
adımlarını gösterirken bana kodları nereye ve hangi dizine yazmam gerektiğini de belirt.
projeyi aşağıdaki dizindeki sanal makinede yapacağım:

/home/train/mlops4/BIST_MLops/  --> yapıldı


çok basit , projeyi bitirmem için aşağıdakileri yapmam lazım:

## Final projesi 

### 1. Veri seti
https://github.com/okankoken/BIST_MLOps/blob/main/data/bist_tum_hisseler_temizlenmis.csv adresindeki  veriyi kullanınız.  --> yapıldı

### 2. Modelleme

2.3.MAkine Öğrenmesi modellemesi yapılarak hangi hisselerin sadece 3 aylık süreçte en fazla getiri sağlayacağının analizi yapılması . verisetindeki bağımsız değişkenler ve finans literatürü baz alınacak. --> yapıldı.
- 2.3. ML Pipeline kullanınız. --> yapıldı



### 3. Deployment
- 3.1. 3 ay  endpoint olacak şekilde bir API geliştiriniz.  --> yapıldı
- 3.2. 3 ay için bir path veya query parameter olarak kullanılsın. --> yapıldı
- 3.3. Fast API sonuç olarak istek yapılan 3 aylık tahmini yüzdelik getiri miktarını dönsün. --> yapldı
- 3.4. Model Concept/Data driftini tespit eden bir mekanizma oluşturunuz.
- 3.5. Model dağıtımı otomasyonu için Jenkins/Gitea kullanınız.

### 4. Altyapı (Infrastructure)
- 4.1. Altyapı olarak Docker container kullanınız.
- 4.2. Veri tabanı olarak mysql kullanınız.
- 4.3. Tahmin sonuçlarını veri tabanına yazınız.