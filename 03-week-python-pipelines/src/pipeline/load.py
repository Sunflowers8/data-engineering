import pandas as pd


def load_to_csv(df: pd.DataFrame, output_path: str) -> None:
    df.to_csv(output_path, index=False)


def load_to_postgres(df: pd.DataFrame, engine, table_name: str) -> None:
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )