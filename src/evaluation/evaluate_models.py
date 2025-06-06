import os
import json
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from ..models.chatgpt_model import ChatGPTModel
from ..models.gemini_model import GeminiModel
from ..models.perplexity_model import PerplexityModel

class ModelEvaluator:
    def __init__(self):
        self.chatgpt = ChatGPTModel()
        self.gemini = GeminiModel()
        self.perplexity = PerplexityModel()
        self.results_dir = "results"
        
        # Sonuçlar için klasör oluştur
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def evaluate_problem(self, problem_text, correct_solution):
        """
        Bir problemi tüm modeller için değerlendirir.
        
        Args:
            problem_text (str): Değerlendirilecek problem
            correct_solution (str): Doğru çözüm
            
        Returns:
            dict: Her model için değerlendirme sonuçları
        """
        results = {}
        
        # Her model için problemi çöz
        for model_name, model in [
            ("ChatGPT", self.chatgpt),
            ("Gemini", self.gemini),
            ("Perplexity", self.perplexity)
        ]:
            try:
                solution = model.solve_problem(problem_text)
                if solution:
                    results[model_name] = {
                        "solution": solution["solution"],
                        "steps": solution["steps"],
                        "correct_solution": correct_solution
                    }
            except Exception as e:
                print(f"{model_name} değerlendirme hatası: {str(e)}")
                results[model_name] = None
        
        return results

    def evaluate_dataset(self, category):
        """
        Belirli bir kategorideki tüm problemleri değerlendirir.
        
        Args:
            category (str): Değerlendirilecek kategori
        """
        try:
            # Kategori veri setini oku
            df = pd.read_csv(f"data/{category.lower().replace(' ', '_')}.csv")
            
            # Sonuçları saklamak için liste
            all_results = []
            
            # Her problemi değerlendir
            for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Değerlendiriliyor: {category}"):
                results = self.evaluate_problem(row['problem_text'], row['solution'])
                all_results.append({
                    "problem": row['problem_text'],
                    "results": results
                })
            
            # Sonuçları kaydet
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.results_dir, f"{category}_{timestamp}.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, ensure_ascii=False, indent=2)
            
            print(f"Değerlendirme sonuçları kaydedildi: {output_file}")
            
        except Exception as e:
            print(f"Veri seti değerlendirme hatası: {str(e)}")

def main():
    evaluator = ModelEvaluator()
    
    # Tüm kategorileri değerlendir
    data_dir = "data"
    for file in os.listdir(data_dir):
        if file.endswith(".csv"):
            category = file.replace(".csv", "").replace("_", " ").title()
            evaluator.evaluate_dataset(category)

if __name__ == "__main__":
    main() 