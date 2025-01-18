# İstanbul Kültür Üniversitesi Kütüphane Chatbotu  

Bu proje, **İstanbul Kültür Üniversitesi** kütüphane sistemi için geliştirilmiş bir chatbot uygulamasıdır. Kullanıcılar, kütüphaneyle ilgili sıkça sorulan sorulara (FAQ) yanıt bulabilir, kütüphane hizmetleri hakkında bilgi alabilir ve doğal bir kullanıcı arayüzü üzerinden chatbot ile etkileşim kurabilir.  

## Özellikler  
- **Soru-Cevap Sistemi:** JSON formatında sağlanan sıkça sorulan sorulara (FAQ) yanıt verir.  
- **Doğal Dil İşleme:** Kullanıcı sorgularını anlamak ve yanıtlamak için metin ön işleme, TF-IDF ve benzerlik analizi kullanır.  
- **Basit ve Şık Arayüz:** Kullanıcı dostu bir PyQt5 tabanlı masaüstü uygulaması sunar.  
- **Türkçe Dil Desteği:** Türkçe stopwords (durak kelimeleri) filtreleme ve dil işleme ile optimize edilmiştir.  

## Ekran Görüntüsü  

*Uygulamayı çalıştırdığımızda bizi karşılayan ekran ve konuşma örneği:*  

<div style="display: flex; gap: 10px;">
    <img src="https://github.com/user-attachments/assets/f4baa36b-ce8d-451e-8180-fcdca4b4de03" alt="Giriş" width="400" height="320">
    <img src="https://github.com/user-attachments/assets/59d6b835-05d0-4572-9b51-f0da19641653" alt="Sorular" width="400" height="320">
</div>


## Kullanılan Teknolojiler  
- **Python:** Ana programlama dili.  
- **PyQt5:** Kullanıcı arayüzü için.  
- **NLTK:** Doğal dil işleme için durak kelime filtreleme.  
- **Scikit-learn:** TF-IDF vektörizasyonu ve benzerlik analizi.  
- **JSON:** Sıkça sorulan sorular (FAQ) veri formatı.  

### Gereksinimler  
- Python 3.8 veya üzeri  
- Gerekli bağımlılıkları yüklemek için aşağıdaki komutu çalıştırın:  
```bash
pip install -r requirements.txt

