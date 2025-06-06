from models.chatgpt_model import ChatGPTModel
from models.gemini_model import GeminiModel
from models.perplexity_model import PerplexityModel
from evaluation.problem_evaluator import ProblemEvaluator
from utils.data_loader import DataLoader
from utils.result_analyzer import ResultAnalyzer
from utils.config import Config
import json
import os
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('evaluation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MathProblemEvaluator:
    def __init__(self):
        self.config = Config()
        self.models = {
            'chatgpt': ChatGPTModel(),
            'gemini': GeminiModel(),
            'perplexity': PerplexityModel()
        }
        self.evaluator = ProblemEvaluator()
        self.data_loader = DataLoader()
        self.result_analyzer = ResultAnalyzer()

    def evaluate_problems(self, problems: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate a list of problems using all available models."""
        results = {}
        
        for problem in problems:
            problem_id = problem['problem_id']
            logger.info(f"Evaluating problem: {problem_id}")
            
            model_responses = {}
            for model_name, model in self.models.items():
                try:
                    response = model.generate_response(problem['question'])
                    model_responses[model_name] = response
                except Exception as e:
                    logger.error(f"Error with {model_name}: {str(e)}")
                    model_responses[model_name] = None
            
            # Evaluate responses
            evaluation_results = self.evaluator.evaluate_responses(problem, model_responses)
            results[problem_id] = evaluation_results
            
            # Save individual problem results
            self.result_analyzer.save_results(evaluation_results, f"problem_{problem_id}.json")
        
        return results

    def analyze_results(self, results):
        """
        Analyze evaluation results and generate insights
        """
        return self.result_analyzer.analyze(results)

def main():
    try:
        # Create .env template if it doesn't exist
        if not os.path.exists('.env'):
            Config.create_env_template()
            print("\nPlease set up your API keys in the .env file and run the program again.")
            return
            
        evaluator = MathProblemEvaluator()
        
        print("Mathematical Problem Evaluation System")
        print("=====================================")
        
        # Get available models
        available_models = list(evaluator.models.keys())
        print(f"Available models: {', '.join(available_models)}")
        
        # Get random problems
        problems = evaluator.data_loader.get_random_problems(count=10)
        print(f"\nSelected {len(problems)} random problems for evaluation.")
        
        # Evaluate problems
        results = evaluator.evaluate_problems(problems)
        
        # Analyze results
        analysis = evaluator.analyze_results(results)
        
        # Save analysis
        evaluator.result_analyzer.save_analysis(analysis)
        
        print("\nEvaluation complete! Results saved in the 'results' directory.")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPlease make sure you have set up your API keys correctly in the .env file.")

if __name__ == "__main__":
    main() 