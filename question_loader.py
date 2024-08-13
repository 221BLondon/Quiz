# question_loader.py
import pandas as pd
from pathlib import Path

# Load questions from CSV file
def load_questions(file_path):
    DATA_FILENAME = Path(__file__).parent / 'new.csv'
    return pd.read_csv(DATA_FILENAME)
