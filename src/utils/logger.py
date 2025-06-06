"""
Logger Module

This module provides comprehensive logging functionality for the application,
including error handling, performance monitoring, and system status tracking.
"""

import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any
import json
import traceback
from pathlib import Path

class Logger:
    """A comprehensive logging system for the application."""
    
    def __init__(
        self,
        log_dir: str = 'logs',
        log_level: int = logging.INFO,
        max_log_files: int = 5
    ):
        """
        Initialize the logger.
        
        Args:
            log_dir (str): Directory to store log files
            log_level (int): Logging level (default: INFO)
            max_log_files (int): Maximum number of log files to keep
        """
        self.log_dir = log_dir
        self.log_level = log_level
        self.max_log_files = max_log_files
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Set up logging configuration
        self._setup_logging()
        
        # Initialize performance metrics
        self.performance_metrics: Dict[str, Any] = {
            'start_time': datetime.now(),
            'operations': {},
            'errors': {},
            'warnings': {}
        }
        
    def _setup_logging(self):
        """Set up logging configuration."""
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # Set up file handler
        log_file = os.path.join(
            self.log_dir,
            f'app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(self.log_level)
        
        # Set up console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(self.log_level)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        # Clean up old log files
        self._cleanup_old_logs()
        
    def _cleanup_old_logs(self):
        """Remove old log files if exceeding max_log_files."""
        log_files = sorted(
            Path(self.log_dir).glob('app_*.log'),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        for old_file in log_files[self.max_log_files:]:
            try:
                old_file.unlink()
            except Exception as e:
                print(f"Error deleting old log file {old_file}: {e}")
                
    def log_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        level: int = logging.ERROR
    ):
        """
        Log an error with context information.
        
        Args:
            error (Exception): The error to log
            context (Dict[str, Any], optional): Additional context information
            level (int): Logging level for the error
        """
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now().isoformat(),
            'context': context or {}
        }
        
        # Log to file
        logging.error(
            f"Error: {error_info['error_type']} - {error_info['error_message']}"
        )
        logging.debug(f"Error details: {json.dumps(error_info, indent=2)}")
        
        # Update performance metrics
        if error_info['error_type'] not in self.performance_metrics['errors']:
            self.performance_metrics['errors'][error_info['error_type']] = 0
        self.performance_metrics['errors'][error_info['error_type']] += 1
        
    def log_warning(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Log a warning with context information.
        
        Args:
            message (str): Warning message
            context (Dict[str, Any], optional): Additional context information
        """
        warning_info = {
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'context': context or {}
        }
        
        # Log to file
        logging.warning(message)
        logging.debug(f"Warning details: {json.dumps(warning_info, indent=2)}")
        
        # Update performance metrics
        if message not in self.performance_metrics['warnings']:
            self.performance_metrics['warnings'][message] = 0
        self.performance_metrics['warnings'][message] += 1
        
    def log_info(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Log an informational message with context.
        
        Args:
            message (str): Information message
            context (Dict[str, Any], optional): Additional context information
        """
        info_data = {
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'context': context or {}
        }
        
        logging.info(message)
        logging.debug(f"Info details: {json.dumps(info_data, indent=2)}")
        
    def log_performance(
        self,
        operation: str,
        duration: float,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Log performance metrics for an operation.
        
        Args:
            operation (str): Name of the operation
            duration (float): Duration in seconds
            context (Dict[str, Any], optional): Additional context information
        """
        perf_info = {
            'operation': operation,
            'duration': duration,
            'timestamp': datetime.now().isoformat(),
            'context': context or {}
        }
        
        # Log to file
        logging.info(
            f"Performance: {operation} took {duration:.2f} seconds"
        )
        logging.debug(f"Performance details: {json.dumps(perf_info, indent=2)}")
        
        # Update performance metrics
        if operation not in self.performance_metrics['operations']:
            self.performance_metrics['operations'][operation] = {
                'count': 0,
                'total_duration': 0,
                'min_duration': float('inf'),
                'max_duration': 0
            }
            
        metrics = self.performance_metrics['operations'][operation]
        metrics['count'] += 1
        metrics['total_duration'] += duration
        metrics['min_duration'] = min(metrics['min_duration'], duration)
        metrics['max_duration'] = max(metrics['max_duration'], duration)
        
    def get_performance_report(self) -> Dict[str, Any]:
        """
        Generate a performance report.
        
        Returns:
            Dict containing performance metrics and statistics
        """
        report = {
            'runtime': (datetime.now() - self.performance_metrics['start_time']).total_seconds(),
            'operations': {},
            'errors': self.performance_metrics['errors'],
            'warnings': self.performance_metrics['warnings']
        }
        
        # Calculate operation statistics
        for op, metrics in self.performance_metrics['operations'].items():
            report['operations'][op] = {
                'count': metrics['count'],
                'average_duration': metrics['total_duration'] / metrics['count'],
                'min_duration': metrics['min_duration'],
                'max_duration': metrics['max_duration']
            }
            
        return report
        
    def save_performance_report(self, output_file: str):
        """
        Save performance report to a file.
        
        Args:
            output_file (str): Path to save the report
        """
        report = self.get_performance_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
            
    def clear_performance_metrics(self):
        """Reset performance metrics."""
        self.performance_metrics = {
            'start_time': datetime.now(),
            'operations': {},
            'errors': {},
            'warnings': {}
        } 