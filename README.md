# Mathematical Problem Evaluation System

A comprehensive Python-based system that evaluates and compares the mathematical problem-solving capabilities of different AI models (ChatGPT, Gemini, and Perplexity). The system automatically analyzes model responses, generates detailed performance metrics, and provides visual insights into model capabilities.

## Features

- **Multi-Model Support**: ChatGPT, Gemini, and Perplexity models
- **Automatic Evaluation**: Automated problem solution evaluation
- **Detailed Analysis**: Performance metrics and statistics for each model
- **Visualization**: Visual performance comparisons through graphs
- **Category-Based Analysis**: Model performance analysis by problem categories
- **Step Analysis**: Detailed analysis of solution steps
- **Error Analysis**: Comprehensive analysis of incorrect answers

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
GOOGLE_API_KEY=your_google_api_key
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
1. List available models
2. Select 10 random problems from the data directory
3. Solve each problem using all models
4. Analyze and visualize the results
5. Save all results in the `results` directory

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
├── requirements.txt
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

## Requirements

- Python 3.8+
- openai
- google-generativeai
- requests
- python-dotenv
- matplotlib
- seaborn
- pandas

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

Error messages are logged in `evaluation.log`.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contact

Project Owner - [@karamustafa10](https://github.com/karamustafa10)

Project Link: [https://github.com/karamustafa10/mathematical-problem-evaluation](https://github.com/karamustafa10/mathematical-problem-evaluation) 