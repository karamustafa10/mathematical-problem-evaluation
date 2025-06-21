"""
Result Analyzer Module for Mathematical Problem Evaluation System.

This module handles the analysis and visualization of evaluation results from different
AI models. It provides functionality to analyze model performance, generate statistics,
and create visualizations of the results.
"""

import json
import os
import logging
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

logger = logging.getLogger(__name__)

class ResultAnalyzer:
    """
    Class for analyzing and visualizing evaluation results.
    
    This class provides methods to:
    - Analyze model performance
    - Generate statistics
    - Create visualizations
    - Save results and analysis
    """

    def __init__(self, results_dir: str = "results"):
        """Initialize the ResultAnalyzer with necessary paths and configurations."""
        self.results_dir = results_dir
        self._create_directories()
        
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('analysis.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.results_dir, exist_ok=True)

    def analyze(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze evaluation results and generate insights.
        
        Args:
            results: Dictionary containing evaluation results for all problems.
            
        Returns:
            Dictionary containing analysis results including statistics and
            performance metrics for each model.
        """
        try:
            analysis = {
                'timestamp': datetime.now().isoformat(),
                'overall_statistics': self._calculate_overall_statistics(results),
                'model_performance': self._analyze_model_performance(results),
                'step_analysis': self._analyze_steps(results),
                'error_analysis': self._analyze_errors(results),
                'category_performance': self._analyze_categories(results)
            }
            return analysis
        except Exception as e:
            logger.error(f"Error in analyze: {str(e)}")
            raise

    def _calculate_overall_statistics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall statistics from results."""
        stats = {
            'total_problems': len(results),
            'correct_answers': {'chatgpt': 0, 'gemini': 0, 'perplexity': 0},
            'incorrect_answers': {'chatgpt': 0, 'gemini': 0, 'perplexity': 0},
            'accuracy': {'chatgpt': 0.0, 'gemini': 0.0, 'perplexity': 0.0}
        }
        
        for problem_id, problem_results in results.items():
            for model, evaluation in problem_results.get('model_evaluations', {}).items():
                if evaluation.get('correctness', {}).get('is_correct', False):
                    stats['correct_answers'][model] += 1
                else:
                    stats['incorrect_answers'][model] += 1
        
        # Calculate accuracy
        for model in stats['accuracy']:
            total = stats['correct_answers'][model] + stats['incorrect_answers'][model]
            if total > 0:
                stats['accuracy'][model] = stats['correct_answers'][model] / total
        
        return stats

    def _analyze_model_performance(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance of each model."""
        performance = {}
        
        for model in ['chatgpt', 'gemini', 'perplexity']:
            total = 0
            correct = 0
            total_steps = 0
            
            for problem_results in results.values():
                evaluation = problem_results.get('model_evaluations', {}).get(model, {})
                if evaluation:
                    total += 1
                    if evaluation.get('correctness', {}).get('is_correct', False):
                        correct += 1
                    total_steps += evaluation.get('step_analysis', {}).get('step_count', 0)
            
            performance[model] = {
                'total': total,
                'correct': correct,
                'accuracy': correct / total if total > 0 else 0.0,
                'avg_steps': total_steps / total if total > 0 else 0.0
            }
        
        return performance

    def _analyze_steps(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze solution steps across all problems."""
        step_analysis = {'chatgpt': {}, 'gemini': {}, 'perplexity': {}}
        
        for problem_results in results.values():
            for model, evaluation in problem_results.get('model_evaluations', {}).items():
                step_types = evaluation.get('step_analysis', {}).get('step_types', {})
                for step_type, count in step_types.items():
                    step_analysis[model][step_type] = step_analysis[model].get(step_type, 0) + count
        
        return step_analysis

    def _analyze_errors(self, results: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze errors made by each model."""
        errors = {'chatgpt': [], 'gemini': [], 'perplexity': []}
        
        for problem_id, problem_results in results.items():
            for model, evaluation in problem_results.get('model_evaluations', {}).items():
                if not evaluation.get('correctness', {}).get('is_correct', False):
                    errors[model].append({
                        'problem_id': problem_id,
                        'expected': problem_results.get('correct_answer', ''),
                        'received': evaluation.get('correctness', {}).get('matched_answer', '')
                    })
        
        return errors

    def _analyze_categories(self, results: Dict[str, Any]) -> Dict[str, Dict[str, int]]:
        """Analyze performance by each model's predicted category."""
        categories = {}
        models = ['chatgpt', 'gemini', 'perplexity']
        for model in models:
            for problem_results in results.values():
                evaluation = problem_results.get('model_evaluations', {}).get(model, {})
                if evaluation and evaluation.get('correctness', {}).get('is_correct', False):
                    predicted_category = evaluation.get('predicted_category', 'unknown')
                    if not predicted_category:
                        predicted_category = 'unknown'
                    if predicted_category not in categories:
                        categories[predicted_category] = {m: 0 for m in models}
                    categories[predicted_category][model] += 1
        return categories

    def save_results(self, results: Dict[str, Any], filename: str) -> None:
        """
        Save evaluation results to a JSON file.
        
        Args:
            results: Dictionary containing evaluation results.
            filename: Name of the file to save results to.
        """
        try:
            file_path = os.path.join(self.results_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Results saved to {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
            raise

    def save_analysis(self, analysis: Dict[str, Any]) -> None:
        """
        Save analysis results and generate visualizations.
        
        Args:
            analysis: Dictionary containing analysis results.
        """
        try:
            file_path = os.path.join(self.results_dir, 'final_analysis.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Analysis saved to {file_path}")
            
            # Generate visualizations
            self._generate_visualizations(analysis)
            
        except Exception as e:
            self.logger.error(f"Error saving analysis: {str(e)}")
            raise

    def _generate_visualizations(self, analysis: Dict[str, Any]):
        """
        Generate and save visualizations of the analysis results.
        
        Args:
            analysis: Dictionary containing analysis results.
        """
        try:
            # Model accuracy plot
            self._plot_model_accuracy(analysis["overall_statistics"]["accuracy"])
            
            # Step analysis plot
            self._plot_step_analysis(analysis["step_analysis"])
            
            # Category performance plot
            self._plot_category_performance(analysis["category_performance"])
            
        except Exception as e:
            self.logger.error(f"Error generating visualizations: {str(e)}")
            raise

    def _plot_model_accuracy(self, accuracy: Dict[str, float]):
        """Plot model accuracy comparison"""
        plt.figure(figsize=(10, 6))
        models = list(accuracy.keys())
        accuracies = list(accuracy.values())
        
        plt.bar(models, accuracies)
        plt.title('Model Accuracy Comparison')
        plt.xlabel('Models')
        plt.ylabel('Accuracy')
        plt.ylim(0, 1)
        
        # Add value labels on top of bars
        for i, v in enumerate(accuracies):
            plt.text(i, v + 0.02, f'{v:.2%}', ha='center')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'model_accuracy.png'))
        plt.close()

    def _plot_step_analysis(self, step_analysis: Dict[str, Dict[str, int]]):
        """Plot step analysis comparison"""
        plt.figure(figsize=(12, 6))
        
        # Prepare data
        models = list(step_analysis.keys())
        step_types = set()
        for model_steps in step_analysis.values():
            step_types.update(model_steps.keys())
        step_types = sorted(list(step_types))
        
        # Create grouped bar chart
        x = range(len(models))
        width = 0.8 / len(step_types)
        
        for i, step_type in enumerate(step_types):
            values = [step_analysis[model].get(step_type, 0) for model in models]
            plt.bar([xi + i * width for xi in x], values, width, label=step_type)
        
        plt.title('Step Analysis by Model')
        plt.xlabel('Models')
        plt.ylabel('Number of Steps')
        plt.xticks([xi + width * (len(step_types) - 1) / 2 for xi in x], models)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'step_analysis.png'))
        plt.close()

    def _plot_category_performance(self, category_performance: Dict[str, Dict[str, int]]):
        """Plot category performance comparison"""
        plt.figure(figsize=(12, 6))
        
        # Prepare data
        categories = list(category_performance.keys())
        models = set()
        for cat_perf in category_performance.values():
            models.update(cat_perf.keys())
        models = sorted(list(models))
        
        # Create grouped bar chart
        x = range(len(categories))
        width = 0.8 / len(models)
        
        for i, model in enumerate(models):
            values = [category_performance[cat].get(model, 0) for cat in categories]
            plt.bar([xi + i * width for xi in x], values, width, label=model)
        
        plt.title('Category Performance by Model')
        plt.xlabel('Categories')
        plt.ylabel('Number of Correct Answers')
        plt.xticks([xi + width * (len(models) - 1) / 2 for xi in x], categories, rotation=45)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, 'category_performance.png'))
        plt.close() 