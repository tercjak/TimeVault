from abc import ABC, abstractmethod

import pandas as pd


class DataProcessor(ABC):
    @abstractmethod
    def process(self, symbol, df: pd.DataFrame) -> pd.DataFrame:
        pass


class BinanceDefaultProcessor(DataProcessor):
    def process(self, symbol, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns={
            "Open time": "ds",
            "Open": symbol
        })
        return df[["ds", df.columns[1]]]  # Return only 'ds' and the price column
