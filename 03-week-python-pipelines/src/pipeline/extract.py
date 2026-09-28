import pandas as pd

def extract_parquet(file_path: str) -> pd.DataFrame:
    df = pd.read_parquet(file_path)
    return df