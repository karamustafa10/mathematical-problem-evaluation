"""
Result analysis module for analyzing and visualizing evaluation results.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
import matplotlib.pyplot as plt
import seaborn as sns

class ResultAnalyzer:
    """Analyzes and visualizes evaluation results."""
    
    def __init__(self, results_file: str):
        """
        Initialize the ResultAnalyzer.
        
        Args:
            results_file: Path to the results JSON file
        """
        self.logger = logging.getLogger(__name__)
        self.results_file = results_file
        self.results = None
        self.output_dir = os.path.dirname(results_file)
        
    def load_results(self) -> None:
        """Load evaluation results from file."""
        try:
            with open(self.results_file, 'r', encoding='utf-8') as f:
                self.results = json.load(f)
            self.logger.info(f"Successfully loaded results from {self.results_file}")
        except Exception as e:
            self.logger.error(f"Error loading results: {str(e)}")
            raise ValueError(f"Failed to load results: {str(e)}")
            
    def calculate_metrics(self) -> Dict[str, Any]:
        """
        Calculate evaluation metrics from results.
        
        Returns:
            Dictionary containing calculated metrics
        """
        if not self.results:
            raise ValueError("No results loaded. Call load_results() first.")
            
        metrics = {
            'overall_accuracy': self._calculate_overall_accuracy(),
            'model_performance': self._calculate_model_performance(),
            'step_completeness': self._calculate_step_completeness()
        }
        
        return metrics
        
    def generate_visualizations(self) -> None:
        """Generate visualization plots for the results."""
        if not self.results:
            raise ValueError("No results loaded. Call load_results() first.")
            
        # Set style
        plt.style.use('default')
        
        # Generate plots
        self._plot_accuracy_comparison()
        self._plot_step_completeness()
        self._plot_step_count_distribution()
        
    def generate_report(self) -> str:
        """
        Generate analysis report.
        
        Returns:
            Path to the generated report file
        """
        if not self.results:
            raise ValueError("No results loaded. Call load_results() first.")
            
        metrics = self.calculate_metrics()
        
        # Generate report content
        report_content = [
            "# Evaluation Results Analysis\n",
            "## Overall Results",
            f"- Overall Accuracy: {metrics['overall_accuracy']:.2%}\n",
            "## Model Performance",
            "### Accuracy by Model"
        ]
        
        for model, perf in metrics['model_performance'].items():
            report_content.append(f"- {model}: {perf['accuracy']:.2%}")
            
        report_content.extend([
            "\n### Step Completeness",
            "Average completeness scores by model:"
        ])
        
        for model, score in metrics['step_completeness'].items():
            report_content.append(f"- {model}: {score:.2%}")
            
        report_content.extend([
            "\n## Visualizations",
            "The following visualizations have been generated:",
            "- Accuracy comparison across models",
            "- Step completeness analysis",
            "- Step count distribution"
        ])
        
        # Save report
        report_path = os.path.join(self.output_dir, 'analysis_report.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_content))
            
        return report_path
        
    def _calculate_overall_accuracy(self) -> float:
        """
        Calculate overall accuracy across all models.
        
        Returns:
            Overall accuracy as a float between 0 and 1
        """
        correct_count = 0
        total_count = 0
        
        for model_result in self.results.values():
            if isinstance(model_result, dict) and 'is_correct' in model_result:
                total_count += 1
                if model_result['is_correct']:
                    correct_count += 1
                    
        return correct_count / total_count if total_count > 0 else 0.0
        
    def _calculate_model_performance(self) -> Dict[str, Dict[str, Any]]:
        """
        Calculate performance metrics for each model.
        
        Returns:
            Dictionary containing performance metrics by model
        """
        performance = {}
        
        for model, result in self.results.items():
            if not isinstance(result, dict):
                continue
                
            performance[model] = {
                'accuracy': result.get('is_correct', False),
                'average_steps': result.get('step_analysis', {}).get('step_count', 0)
            }
            
        return performance
        
    def _calculate_step_completeness(self) -> Dict[str, float]:
        """
        Calculate step completeness scores for each model.
        
        Returns:
            Dictionary containing completeness scores by model
        """
        completeness = {}
        
        for model, result in self.results.items():
            if not isinstance(result, dict):
                continue
                
            step_analysis = result.get('step_analysis', {})
            completeness[model] = step_analysis.get('completeness', 0.0)
            
        return completeness
        
    def _plot_accuracy_comparison(self) -> None:
        """Generate accuracy comparison plot."""
        plt.figure(figsize=(10, 6))
        
        models = []
        accuracies = []
        
        for model, result in self.results.items():
            if isinstance(result, dict) and 'is_correct' in result:
                models.append(model)
                accuracies.append(float(result['is_correct']))
                
        plt.bar(models, accuracies)
        plt.title('Model Accuracy Comparison')
        plt.xlabel('Model')
        plt.ylabel('Accuracy')
        plt.ylim(0, 1)
        
        # Save plot
        plt.savefig(os.path.join(self.output_dir, 'accuracy_comparison.png'))
        plt.close()
        
    def _plot_step_completeness(self) -> None:
        """Generate step completeness plot."""
        plt.figure(figsize=(10, 6))
        
        models = []
        completeness = []
        
        for model, result in self.results.items():
            if isinstance(result, dict):
                step_analysis = result.get('step_analysis', {})
                models.append(model)
                completeness.append(step_analysis.get('completeness', 0.0))
                
        plt.bar(models, completeness)
        plt.title('Step Completeness by Model')
        plt.xlabel('Model')
        plt.ylabel('Completeness Score')
        plt.ylim(0, 1)
        
        # Save plot
        plt.savefig(os.path.join(self.output_dir, 'step_completeness.png'))
        plt.close()
        
    def _plot_step_count_distribution(self) -> None:
        """Generate step count distribution plot."""
        plt.figure(figsize=(10, 6))
        
        step_counts = []
        
        for result in self.results.values():
            if isinstance(result, dict):
                step_analysis = result.get('step_analysis', {})
                step_counts.append(step_analysis.get('step_count', 0))
                
        sns.histplot(step_counts, bins=10)
        plt.title('Distribution of Step Counts')
        plt.xlabel('Number of Steps')
        plt.ylabel('Frequency')
        
        # Save plot
        plt.savefig(os.path.join(self.output_dir, 'step_count_distribution.png'))
        plt.close() 