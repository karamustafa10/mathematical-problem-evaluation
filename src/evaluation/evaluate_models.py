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
        
        # Create a folder for results
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def evaluate_problem(self, problem_text, correct_solution):
        """
        Evaluates a problem for all models.
        
        Args:
            problem_text (str): The problem to be evaluated
            correct_solution (str): The correct solution
            
        Returns:
            dict: Evaluation results for each model
        """
        results = {}
        
        # Solve the problem for each model
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
                print(f"{model_name} evaluation error: {str(e)}")
                results[model_name] = None
        
        return results

    def evaluate_dataset(self, category):
        """
        Evaluates all problems in a specific category.
        
        Args:
            category (str): The category to be evaluated
        """
        try:
            # Read the category dataset
            df = pd.read_csv(f"data/{category.lower().replace(' ', '_')}.csv")
            
            # List to store results
            all_results = []
            
            # Evaluate each problem
            for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Evaluating: {category}"):
                results = self.evaluate_problem(row['problem_text'], row['solution'])
                all_results.append({
                    "problem": row['problem_text'],
                    "results": results
                })
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.results_dir, f"{category}_{timestamp}.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, ensure_ascii=False, indent=2)
            
            print(f"Evaluation results saved: {output_file}")
            
        except Exception as e:
            print(f"Dataset evaluation error: {str(e)}")

def main():
    evaluator = ModelEvaluator()
    
    # Evaluate all categories
    data_dir = "data"
    for file in os.listdir(data_dir):
        if file.endswith(".csv"):
            category = file.replace(".csv", "").replace("_", " ").title()
            evaluator.evaluate_dataset(category)

if __name__ == "__main__":
    main() 