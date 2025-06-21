# Mathematical Problem Evaluation System

A comprehensive Python-based system that evaluates and compares the mathematical problem-solving capabilities of different AI models (ChatGPT, Gemini, and Perplexity). The system automatically analyzes model responses, generates detailed performance metrics, and provides visual insights into model capabilities.

## Features

- **Multi-Model Support**: ChatGPT, Gemini, and Perplexity models
- **Automatic Evaluation**: Automated problem solution evaluation with detailed logging
- **Detailed Analysis**: Performance metrics and statistics for each model
- **Visualization**: Visual performance comparisons through graphs
- **Category-Based Analysis**: Model performance analysis by problem categories
- **Step Analysis**: Detailed analysis of solution steps
- **Error Analysis**: Comprehensive analysis of incorrect answers
- **Logging**: Detailed logging of evaluation process and errors
- **Progress Tracking**: Progress bars for long-running operations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/karamustafa10/mathematical-problem-evaluation.git
cd mathematical-problem-evaluation
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key
```

## Data Preparation

### Option 1: Using Sample Data
The system will automatically create a sample problem if no data files are found in the `data` directory.

### Option 2: Using Custom Data
1. Create a `data` directory in the project root:
```bash
mkdir data
```

2. Prepare your CSV files with the following structure:
```csv
problem_id,problem,answer,solution,category,difficulty
1,"What is the sum of all positive integers less than 100 that are divisible by 3?","1683","Step 1: Identify numbers...","arithmetic","medium"
```

Required columns:
- `problem_id`: Unique identifier for the problem
- `problem`: The problem text
- `answer`: Correct answer
- `solution`: Step-by-step solution
- `category`: Problem category (arithmetic, algebra, geometry, etc.)
- `difficulty`: Problem difficulty level (easy, medium, hard)

### Option 3: Using AIME Problems
1. Download AIME problems from the official website
2. Convert the problems to the required CSV format
3. Place the CSV files in the `data` directory

## Usage

Run the program:
```bash
python src/main.py
```

The program will:
1. Check for API keys and create a template if missing
2. List available models
3. Select 10 random problems from the data directory
4. Solve each problem using all models
5. Analyze and visualize the results
6. Save all results in the `results` directory
7. Generate detailed logs in `evaluation.log`
8. Generate a step-by-step comparative error report in `results/comparison_report.json`

## Project Structure

```
├── src/
│   ├── models/
│   │   ├── chatgpt_model.py
│   │   ├── gemini_model.py
│   │   └── perplexity_model.py
│   ├── evaluation/
│   │   ├── problem_evaluator.py
│   │   └── evaluate_models.py
│   ├── utils/
│   │   ├── data_loader.py
│   │   ├── result_analyzer.py
│   │   └── config.py
│   └── main.py
├── data/
│   └── *.csv (problem files)
├── results/
│   ├── problem_*.json (results for each problem)
│   ├── final_analysis.json (overall analysis)
│   └── *.png (visualizations)
├── tests/
│   └── test_*.py (unit tests)
├── requirements.txt
├── evaluation.log
├── analysis.log
└── .env
```

## Analysis Outputs

The program generates the following analyses:
1. **Overall Statistics**:
   - Total number of problems
   - Correct/incorrect answer counts
   - Model accuracy rates

2. **Model Performance**:
   - Accuracy rate for each model
   - Average number of solution steps
   - Category-based performance

3. **Step Analysis**:
   - Step types used by each model
   - Step count distribution

4. **Error Analysis**:
   - Detailed analysis of incorrect answers
   - Comparison of expected and received answers

5. **Step-by-step Comparative Error Report**:
   - For each problem, compares the steps of correct and incorrect models
   - Shows where the incorrect model made a mistake and how the correct model fixed it
   - Saved as `results/comparison_report.json`

## Requirements

- Python 3.8+
- openai>=1.0.0
- google-generativeai>=0.3.0
- pandas==2.2.1
- numpy==1.26.3
- matplotlib==3.8.2
- seaborn==0.13.1
- python-dotenv>=1.0.0
- requests>=2.31.0
- tqdm==4.66.2

## Troubleshooting

Common issues and solutions:
1. API keys missing or invalid
   - Check your `.env` file
   - Verify API key permissions
2. Data files not found
   - Ensure CSV files are in the `data` directory
   - Check file format and column names
3. Model API access issues
   - Check internet connection
   - Verify API rate limits
   - Check API key quotas

Error messages are logged in `evaluation.log` and `analysis.log`.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Project Owner - [@karamustafa10](https://github.com/karamustafa10)

Project Link: [https://github.com/karamustafa10/mathematical-problem-evaluation](https://github.com/karamustafa10/mathematical-problem-evaluation) 