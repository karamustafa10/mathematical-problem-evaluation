import os
import json
import pandas as pd
import kaggle
from pathlib import Path

def setup_kaggle_credentials():
    """
    Kaggle API kimlik bilgilerini ayarlar.
    """
    try:
        # Kaggle.json dosyasının yolunu belirle
        kaggle_json_path = Path("evraklar/kaggle.json")
        
        if not kaggle_json_path.exists():
            raise FileNotFoundError("kaggle.json dosyası bulunamadı!")
        
        # Kaggle.json dosyasını oku
        with open(kaggle_json_path, 'r') as f:
            credentials = json.load(f)
        
        # Kaggle API kimlik bilgilerini ayarla
        os.environ['KAGGLE_USERNAME'] = credentials['username']
        os.environ['KAGGLE_KEY'] = credentials['key']
        
        print("Kaggle kimlik bilgileri başarıyla ayarlandı.")
        
    except Exception as e:
        print(f"Kaggle kimlik bilgileri ayarlama hatası: {str(e)}")
        raise

def download_dataset():
    """
    Kaggle'dan AMC 8 veri setini indirir ve işler.
    """
    try:
        # Kaggle kimlik bilgilerini ayarla
        setup_kaggle_credentials()
        
        print("Veri seti indiriliyor...")
        
        # Veri setini indir
        dataset = "alexryzhkov/amio-parsed-art-of-problem-solving-website"
        kaggle.api.dataset_download_files(dataset, path="data", unzip=True)
        
        print("Veri seti başarıyla indirildi.")
        
        # Veri setini oku
        df = pd.read_csv("data/parsed_ArtOfProblemSolving.csv")
        
        print("\nVeri seti önizlemesi:")
        print(df.head())
        
        print("\nSütun isimleri:")
        print(df.columns.tolist())
        
        # Veri setini işle
        process_dataset(df)
        
    except Exception as e:
        print(f"Veri seti indirme hatası: {str(e)}")

def process_dataset(df):
    """
    İndirilen veri setini işler ve kategorilere ayırır.
    
    Args:
        df (pandas.DataFrame): İndirilen veri seti
    """
    try:
        # Sütun isimlerini kontrol et ve gerekli sütunları seç
        required_columns = ['problem_id', 'link', 'problem', 'solution', 'letter', 'answer']
        
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Veri setinde gerekli sütunlar bulunamadı. Mevcut sütunlar: {df.columns.tolist()}")
        
        # Gerekli sütunları seç
        df = df[required_columns]
        
        # Kategorilere göre grupla (problem_id'ye göre)
        categories = df['problem_id'].unique()
        
        # Her kategori için ayrı dosya oluştur
        for category in categories:
            category_df = df[df['problem_id'] == category]
            output_path = f"data/problem_{category}.csv"
            category_df.to_csv(output_path, index=False)
            print(f"Problem kaydedildi: {category} -> {output_path}")
        
        print("\nVeri seti başarıyla işlendi ve problemlere ayrıldı.")
        
    except Exception as e:
        print(f"Veri seti işleme hatası: {str(e)}")

if __name__ == "__main__":
    download_dataset() 