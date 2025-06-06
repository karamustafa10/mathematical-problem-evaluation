"""
Result Analyzer Module

This module provides functionality for analyzing and visualizing the results of
mathematical problem evaluations across different AI models.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any
import json
from datetime import datetime
import os

class ResultAnalyzer:
    """Analyzes and visualizes evaluation results from different AI models."""
    
    def __init__(self, results_file: str):
        """
        Initialize the ResultAnalyzer.
        
        Args:
            results_file (str): Path to the JSON file containing evaluation results
        """
        self.results_file = results_file
        self.results = self._load_results()
        
    def _load_results(self) -> Dict:
        """Load results from JSON file."""
        try:
            with open(self.results_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Results file not found: {self.results_file}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {self.results_file}")
            return {}
            
    def calculate_metrics(self) -> Dict[str, Any]:
        """
        Calculate comprehensive evaluation metrics.
        
        Returns:
            Dict containing various evaluation metrics
        """
        metrics = {
            'overall_accuracy': self._calculate_overall_accuracy(),
            'category_accuracy': self._calculate_category_accuracy(),
            'step_completeness': self._calculate_step_completeness(),
            'error_distribution': self._analyze_error_distribution(),
            'response_times': self._analyze_response_times(),
            'model_comparison': self._compare_models()
        }
        return metrics
        
    def _calculate_overall_accuracy(self) -> float:
        """Calculate overall accuracy across all problems and models."""
        total_correct = 0
        total_problems = 0
        
        for problem_id, problem_data in self.results.items():
            for model_name, model_data in problem_data.items():
                if model_data.get('is_correct'):
                    total_correct += 1
                total_problems += 1
                
        return (total_correct / total_problems) * 100 if total_problems > 0 else 0
        
    def _calculate_category_accuracy(self) -> Dict[str, float]:
        """Calculate accuracy for each problem category."""
        category_correct = {}
        category_total = {}
        
        for problem_id, problem_data in self.results.items():
            category = problem_data.get('category', 'unknown')
            for model_name, model_data in problem_data.items():
                if model_name != 'category':  # Skip category entry
                    if category not in category_correct:
                        category_correct[category] = 0
                        category_total[category] = 0
                    if model_data.get('is_correct'):
                        category_correct[category] += 1
                    category_total[category] += 1
                    
        return {
            category: (correct / total) * 100 
            for category, (correct, total) in zip(
                category_correct.keys(),
                zip(category_correct.values(), category_total.values())
            )
        }
        
    def _calculate_step_completeness(self) -> Dict[str, float]:
        """Calculate step completeness for each model."""
        model_steps = {}
        model_total = {}
        
        for problem_id, problem_data in self.results.items():
            for model_name, model_data in problem_data.items():
                if model_name != 'category':  # Skip category entry
                    if model_name not in model_steps:
                        model_steps[model_name] = 0
                        model_total[model_name] = 0
                    steps = model_data.get('steps', [])
                    model_steps[model_name] += len(steps)
                    model_total[model_name] += 1
                    
        return {
            model: steps / total 
            for model, (steps, total) in zip(
                model_steps.keys(),
                zip(model_steps.values(), model_total.values())
            )
        }
        
    def _analyze_error_distribution(self) -> Dict[str, Dict[str, int]]:
        """Analyze distribution of different types of errors."""
        error_types = {}
        
        for problem_id, problem_data in self.results.items():
            for model_name, model_data in problem_data.items():
                if model_name != 'category':  # Skip category entry
                    if not model_data.get('is_correct'):
                        error_type = model_data.get('error_type', 'unknown')
                        if model_name not in error_types:
                            error_types[model_name] = {}
                        if error_type not in error_types[model_name]:
                            error_types[model_name][error_type] = 0
                        error_types[model_name][error_type] += 1
                        
        return error_types
        
    def _analyze_response_times(self) -> Dict[str, Dict[str, float]]:
        """Analyze response times for each model."""
        response_times = {}
        
        for problem_id, problem_data in self.results.items():
            for model_name, model_data in problem_data.items():
                if model_name != 'category':  # Skip category entry
                    if model_name not in response_times:
                        response_times[model_name] = {
                            'total': 0,
                            'count': 0,
                            'min': float('inf'),
                            'max': 0
                        }
                    time = model_data.get('response_time', 0)
                    response_times[model_name]['total'] += time
                    response_times[model_name]['count'] += 1
                    response_times[model_name]['min'] = min(
                        response_times[model_name]['min'],
                        time
                    )
                    response_times[model_name]['max'] = max(
                        response_times[model_name]['max'],
                        time
                    )
                    
        # Calculate averages
        for model in response_times:
            if response_times[model]['count'] > 0:
                response_times[model]['average'] = (
                    response_times[model]['total'] / 
                    response_times[model]['count']
                )
            else:
                response_times[model]['average'] = 0
                
        return response_times
        
    def _compare_models(self) -> Dict[str, Dict[str, float]]:
        """Compare performance metrics across different models."""
        model_metrics = {}
        
        for problem_id, problem_data in self.results.items():
            for model_name, model_data in problem_data.items():
                if model_name != 'category':  # Skip category entry
                    if model_name not in model_metrics:
                        model_metrics[model_name] = {
                            'correct': 0,
                            'total': 0,
                            'steps': 0
                        }
                    if model_data.get('is_correct'):
                        model_metrics[model_name]['correct'] += 1
                    model_metrics[model_name]['total'] += 1
                    model_metrics[model_name]['steps'] += len(
                        model_data.get('steps', [])
                    )
                    
        # Calculate final metrics
        for model in model_metrics:
            if model_metrics[model]['total'] > 0:
                model_metrics[model]['accuracy'] = (
                    model_metrics[model]['correct'] / 
                    model_metrics[model]['total']
                ) * 100
                model_metrics[model]['avg_steps'] = (
                    model_metrics[model]['steps'] / 
                    model_metrics[model]['total']
                )
            else:
                model_metrics[model]['accuracy'] = 0
                model_metrics[model]['avg_steps'] = 0
                
        return model_metrics
        
    def generate_visualizations(self, output_dir: str = 'analysis_output'):
        """
        Generate various visualizations of the evaluation results.
        
        Args:
            output_dir (str): Directory to save visualization files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn')
        
        # 1. Overall Accuracy Bar Chart
        self._plot_overall_accuracy(output_dir)
        
        # 2. Category Accuracy Heatmap
        self._plot_category_accuracy(output_dir)
        
        # 3. Step Completeness Comparison
        self._plot_step_completeness(output_dir)
        
        # 4. Error Distribution
        self._plot_error_distribution(output_dir)
        
        # 5. Response Time Analysis
        self._plot_response_times(output_dir)
        
        # 6. Model Comparison
        self._plot_model_comparison(output_dir)
        
    def _plot_overall_accuracy(self, output_dir: str):
        """Plot overall accuracy bar chart."""
        metrics = self.calculate_metrics()
        accuracy = metrics['overall_accuracy']
        
        plt.figure(figsize=(10, 6))
        plt.bar(['Overall Accuracy'], [accuracy])
        plt.title('Overall Accuracy Across All Models')
        plt.ylabel('Accuracy (%)')
        plt.ylim(0, 100)
        
        # Add value labels
        plt.text(0, accuracy + 2, f'{accuracy:.1f}%', ha='center')
        
        plt.savefig(os.path.join(output_dir, 'overall_accuracy.png'))
        plt.close()
        
    def _plot_category_accuracy(self, output_dir: str):
        """Plot category accuracy heatmap."""
        metrics = self.calculate_metrics()
        category_acc = metrics['category_accuracy']
        
        # Convert to DataFrame for heatmap
        df = pd.DataFrame.from_dict(
            category_acc,
            orient='index',
            columns=['Accuracy']
        )
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(
            df,
            annot=True,
            fmt='.1f',
            cmap='YlOrRd',
            cbar_kws={'label': 'Accuracy (%)'}
        )
        plt.title('Accuracy by Problem Category')
        plt.tight_layout()
        
        plt.savefig(os.path.join(output_dir, 'category_accuracy.png'))
        plt.close()
        
    def _plot_step_completeness(self, output_dir: str):
        """Plot step completeness comparison."""
        metrics = self.calculate_metrics()
        step_comp = metrics['step_completeness']
        
        plt.figure(figsize=(12, 6))
        plt.bar(step_comp.keys(), step_comp.values())
        plt.title('Step Completeness by Model')
        plt.xlabel('Model')
        plt.ylabel('Average Steps per Problem')
        plt.xticks(rotation=45)
        
        # Add value labels
        for i, v in enumerate(step_comp.values()):
            plt.text(i, v + 0.1, f'{v:.1f}', ha='center')
            
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'step_completeness.png'))
        plt.close()
        
    def _plot_error_distribution(self, output_dir: str):
        """Plot error distribution analysis."""
        metrics = self.calculate_metrics()
        error_dist = metrics['error_distribution']
        
        # Convert to DataFrame
        df = pd.DataFrame.from_dict(
            error_dist,
            orient='index'
        ).fillna(0)
        
        plt.figure(figsize=(12, 8))
        df.plot(kind='bar', stacked=True)
        plt.title('Error Distribution by Model')
        plt.xlabel('Model')
        plt.ylabel('Number of Errors')
        plt.legend(title='Error Type', bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        
        plt.savefig(os.path.join(output_dir, 'error_distribution.png'))
        plt.close()
        
    def _plot_response_times(self, output_dir: str):
        """Plot response time analysis."""
        metrics = self.calculate_metrics()
        response_times = metrics['response_times']
        
        # Prepare data for box plot
        data = []
        labels = []
        for model, times in response_times.items():
            if times['count'] > 0:
                data.append([
                    times['min'],
                    times['average'],
                    times['max']
                ])
                labels.append(model)
                
        plt.figure(figsize=(12, 6))
        plt.boxplot(data, labels=labels)
        plt.title('Response Time Distribution by Model')
        plt.xlabel('Model')
        plt.ylabel('Response Time (seconds)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(os.path.join(output_dir, 'response_times.png'))
        plt.close()
        
    def _plot_model_comparison(self, output_dir: str):
        """Plot model comparison metrics."""
        metrics = self.calculate_metrics()
        model_comp = metrics['model_comparison']
        
        # Prepare data
        models = list(model_comp.keys())
        accuracy = [m['accuracy'] for m in model_comp.values()]
        avg_steps = [m['avg_steps'] for m in model_comp.values()]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Accuracy plot
        ax1.bar(models, accuracy)
        ax1.set_title('Model Accuracy Comparison')
        ax1.set_xlabel('Model')
        ax1.set_ylabel('Accuracy (%)')
        ax1.set_ylim(0, 100)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for i, v in enumerate(accuracy):
            ax1.text(i, v + 2, f'{v:.1f}%', ha='center')
            
        # Average steps plot
        ax2.bar(models, avg_steps)
        ax2.set_title('Average Steps per Problem')
        ax2.set_xlabel('Model')
        ax2.set_ylabel('Number of Steps')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for i, v in enumerate(avg_steps):
            ax2.text(i, v + 0.1, f'{v:.1f}', ha='center')
            
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'model_comparison.png'))
        plt.close()
        
    def generate_report(self, output_dir: str = 'analysis_output') -> str:
        """
        Generate a comprehensive analysis report.
        
        Args:
            output_dir (str): Directory to save the report
            
        Returns:
            str: Path to the generated report file
        """
        metrics = self.calculate_metrics()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(output_dir, f'analysis_report_{timestamp}.md')
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('# Mathematical Problem Evaluation Analysis Report\n\n')
            
            # Overall Results
            f.write('## Overall Results\n\n')
            f.write(f'- Overall Accuracy: {metrics["overall_accuracy"]:.1f}%\n\n')
            
            # Category Analysis
            f.write('## Category Analysis\n\n')
            for category, accuracy in metrics['category_accuracy'].items():
                f.write(f'- {category}: {accuracy:.1f}%\n')
            f.write('\n')
            
            # Model Comparison
            f.write('## Model Comparison\n\n')
            for model, data in metrics['model_comparison'].items():
                f.write(f'### {model}\n')
                f.write(f'- Accuracy: {data["accuracy"]:.1f}%\n')
                f.write(f'- Average Steps: {data["avg_steps"]:.1f}\n\n')
                
            # Error Analysis
            f.write('## Error Analysis\n\n')
            for model, errors in metrics['error_distribution'].items():
                f.write(f'### {model}\n')
                for error_type, count in errors.items():
                    f.write(f'- {error_type}: {count}\n')
                f.write('\n')
                
            # Response Time Analysis
            f.write('## Response Time Analysis\n\n')
            for model, times in metrics['response_times'].items():
                f.write(f'### {model}\n')
                f.write(f'- Average: {times["average"]:.2f} seconds\n')
                f.write(f'- Min: {times["min"]:.2f} seconds\n')
                f.write(f'- Max: {times["max"]:.2f} seconds\n\n')
                
            # Recommendations
            f.write('## Recommendations\n\n')
            f.write('1. Model Performance Improvements\n')
            f.write('2. Error Pattern Analysis\n')
            f.write('3. Response Time Optimization\n')
            f.write('4. Category-Specific Enhancements\n')
            
        return report_file 