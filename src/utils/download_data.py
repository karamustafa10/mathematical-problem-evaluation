import os
import json
import pandas as pd
import kaggle
from pathlib import Path

def setup_kaggle_credentials():
    """
    Sets up Kaggle API credentials.
    """
    try:
        # Determine the path of kaggle.json file
        kaggle_json_path = Path("evraklar/kaggle.json")
        
        if not kaggle_json_path.exists():
            raise FileNotFoundError("kaggle.json file not found!")
        
        # Read the kaggle.json file
        with open(kaggle_json_path, 'r') as f:
            credentials = json.load(f)
        
        # Set Kaggle API credentials
        os.environ['KAGGLE_USERNAME'] = credentials['username']
        os.environ['KAGGLE_KEY'] = credentials['key']
        
        print("Kaggle credentials set successfully.")
        
    except Exception as e:
        print(f"Error setting Kaggle credentials: {str(e)}")
        raise

def download_dataset():
    """
    Downloads and processes the AMC 8 dataset from Kaggle.
    """
    try:
        # Set Kaggle credentials
        setup_kaggle_credentials()
        
        print("Downloading dataset...")
        
        # Download the dataset
        dataset = "alexryzhkov/amio-parsed-art-of-problem-solving-website"
        kaggle.api.dataset_download_files(dataset, path="data", unzip=True)
        
        print("Dataset downloaded successfully.")
        
        # Read the dataset
        df = pd.read_csv("data/parsed_ArtOfProblemSolving.csv")
        
        print("\nDataset preview:")
        print(df.head())
        
        print("\nColumn names:")
        print(df.columns.tolist())
        
        # Process the dataset
        process_dataset(df)
        
    except Exception as e:
        print(f"Error downloading dataset: {str(e)}")

def process_dataset(df):
    """
    Processes the downloaded dataset and splits it into categories.
    
    Args:
        df (pandas.DataFrame): The downloaded dataset
    """
    try:
        # Check column names and select required columns
        required_columns = ['problem_id', 'link', 'problem', 'solution', 'letter', 'answer']
        
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Required columns not found in the dataset. Available columns: {df.columns.tolist()}")
        
        # Select required columns
        df = df[required_columns]
        
        # Group by categories (by problem_id)
        categories = df['problem_id'].unique()
        
        # Create a separate file for each category
        for category in categories:
            category_df = df[df['problem_id'] == category]
            output_path = f"data/problem_{category}.csv"
            category_df.to_csv(output_path, index=False)
            print(f"Problem saved: {category} -> {output_path}")
        
        print("\nDataset processed and split into problems successfully.")
        
    except Exception as e:
        print(f"Error processing dataset: {str(e)}")

if __name__ == "__main__":
    download_dataset() 