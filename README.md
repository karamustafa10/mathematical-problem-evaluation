# Matematik Problemi Değerlendirme Sistemi

Bu proje, farklı yapay zeka modellerinin (ChatGPT, Gemini ve Perplexity) matematik problemlerini çözme yeteneklerini değerlendiren ve karşılaştıran bir Python uygulamasıdır.

## Özellikler

- **Çoklu Model Desteği**: ChatGPT, Gemini ve Perplexity modellerini destekler
- **Otomatik Değerlendirme**: Problem çözümlerini otomatik olarak değerlendirir
- **Detaylı Analiz**: Her model için performans metrikleri ve istatistikler
- **Görselleştirme**: Model performanslarını görsel grafiklerle sunar
- **Kategori Bazlı Analiz**: Problem kategorilerine göre model performanslarını analiz eder
- **Adım Analizi**: Çözüm adımlarının detaylı analizi
- **Hata Analizi**: Yanlış cevapların detaylı analizi

## Kurulum

1. Projeyi klonlayın:
```bash
git clone <repo-url>
cd <proje-dizini>
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. `.env` dosyası oluşturun ve API anahtarlarınızı ekleyin:
```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key
```

## Kullanım

Uygulamayı başlatmak için:
```bash
python src/main.py
```

Program otomatik olarak:
1. Kullanılabilir modelleri listeler
2. Veri klasöründen rastgele 10 problem seçer
3. Her problemi tüm modellerle çözer
4. Sonuçları analiz eder ve görselleştirir
5. Tüm sonuçları `results` klasörüne kaydeder

## Proje Yapısı

```
├── src/
│   ├── models/
│   │   ├── chatgpt_model.py
│   │   ├── gemini_model.py
│   │   └── perplexity_model.py
│   ├── evaluation/
│   │   ├── problem_evaluator.py
│   │   └── evaluate_models.py
│   ├── utils/
│   │   ├── data_loader.py
│   │   ├── result_analyzer.py
│   │   └── config.py
│   └── main.py
├── data/
│   └── *.csv (problem dosyaları)
├── results/
│   ├── problem_*.json (her problem için sonuçlar)
│   ├── final_analysis.json (genel analiz)
│   └── *.png (görselleştirmeler)
├── requirements.txt
└── .env
```

## Veri Formatı

Problem dosyaları CSV formatında olmalıdır ve şu sütunları içermelidir:
- `problem_id`: Benzersiz problem tanımlayıcısı
- `problem`: Problem metni
- `answer`: Doğru cevap
- `solution`: Çözüm adımları

## Analiz Çıktıları

Program şu analizleri üretir:
1. **Genel İstatistikler**:
   - Toplam problem sayısı
   - Doğru/yanlış cevap sayıları
   - Model doğruluk oranları

2. **Model Performansı**:
   - Her model için doğruluk oranı
   - Ortalama çözüm adımı sayısı
   - Kategori bazlı performans

3. **Adım Analizi**:
   - Her model için kullanılan adım tipleri
   - Adım sayısı dağılımı

4. **Hata Analizi**:
   - Yanlış cevapların detaylı analizi
   - Beklenen ve alınan cevapların karşılaştırması

## Gereksinimler

- Python 3.8+
- openai
- google-generativeai
- requests
- python-dotenv
- matplotlib
- seaborn
- pandas

## Hata Ayıklama

Program çalışırken oluşabilecek hatalar:
1. API anahtarları eksik veya geçersiz
2. Veri dosyaları bulunamadı
3. Model API'lerine erişim sorunları

Hata mesajları `evaluation.log` dosyasına kaydedilir.

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## İletişim

Proje Sahibi - [@github_username](https://github.com/github_username)

Proje Linki: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name) 