"""
Main module for the Mathematical Problem Evaluation System.

This module serves as the entry point for the application, coordinating the evaluation
of mathematical problems across different AI models (ChatGPT, Gemini, and Perplexity).
It handles the initialization of models, problem loading, evaluation, and result analysis.
"""

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

# Configure logging with both file and console handlers
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
    """
    Main class for evaluating mathematical problems using different AI models.
    
    This class coordinates the entire evaluation process, including:
    - Model initialization
    - Problem loading
    - Response generation
    - Result evaluation
    - Analysis generation
    """

    def __init__(self):
        """Initialize the evaluator with all necessary components."""
        self.config = Config()
        # Initialize all available models
        self.models = {
            'chatgpt': ChatGPTModel(),
            'gemini': GeminiModel(),
            'perplexity': PerplexityModel()
        }
        self.evaluator = ProblemEvaluator()
        self.data_loader = DataLoader()
        self.result_analyzer = ResultAnalyzer()

    def evaluate_problems(self, problems: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate a list of problems using all available models.
        
        Args:
            problems: List of problems to evaluate, each containing problem_id, question,
                     correct_answer, and other metadata.
        
        Returns:
            Dictionary containing evaluation results for each problem.
        """
        results = {}
        
        for problem in problems:
            problem_id = problem['problem_id']
            logger.info(f"Evaluating problem: {problem_id}")
            
            # Get responses from all models
            model_responses = {}
            model_categories = {}
            for model_name, model in self.models.items():
                try:
                    response = model.generate_response(problem['question'])
                    if response and isinstance(response, dict):
                        model_responses[model_name] = response.get('solution', None)
                        model_categories[model_name] = response.get('category', None)
                    else:
                        model_responses[model_name] = response if isinstance(response, str) else None
                        model_categories[model_name] = None
                except Exception as e:
                    logger.error(f"Error with {model_name}: {str(e)}")
                    model_responses[model_name] = None
                    model_categories[model_name] = None
            # Add model categories to the problem dictionary
            problem['model_categories'] = model_categories
            # Evaluate responses and save results
            evaluation_results = self.evaluator.evaluate_responses(problem, model_responses)
            results[problem_id] = evaluation_results
            # Save individual problem results
            self.result_analyzer.save_results(evaluation_results, f"problem_{problem_id}.json")
        return results

    def analyze_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze evaluation results and generate insights.
        
        Args:
            results: Dictionary containing evaluation results for all problems.
        
        Returns:
            Dictionary containing analysis results including statistics, performance metrics,
            and visualizations.
        """
        return self.result_analyzer.analyze(results)

def main():
    """
    Main entry point for the application.
    
    This function:
    1. Checks for API keys
    2. Initializes the evaluator
    3. Loads problems
    4. Runs evaluations
    5. Generates analysis
    6. Saves results
    """
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
        
        # Get random problems for evaluation
        problems = evaluator.data_loader.get_random_problems(count=10)
        print(f"\nSelected {len(problems)} random problems for evaluation.")
        
        # Evaluate problems and generate analysis
        results = evaluator.evaluate_problems(problems)
        analysis = evaluator.analyze_results(results)

        # --- NEW ADDITION: Step-by-step comparative error report ---
        comparison_report = evaluator.result_analyzer.compare_correct_and_incorrect_models(results)
        comparison_path = os.path.join(evaluator.result_analyzer.results_dir, 'comparison_report.json')
        with open(comparison_path, 'w', encoding='utf-8') as f:
            json.dump(comparison_report, f, ensure_ascii=False, indent=2)
        print(f"\nStep-by-step comparative error report has been saved to '{comparison_path}'.")
        # --- END OF NEW ADDITION ---

        # Save final analysis
        evaluator.result_analyzer.save_analysis(analysis)
        
        print("\nEvaluation complete! Results saved in the 'results' directory.")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPlease make sure you have set up your API keys correctly in the .env file.")

if __name__ == "__main__":
    main() 