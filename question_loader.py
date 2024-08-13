# question_loader.py
import pandas as pd
from pathlib import Path

def load_questions(file_path):
    data_filename = Path(file_path)
    return pd.read_csv(data_filename)
