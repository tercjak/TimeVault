from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import pandas as pd
from tqdm import tqdm


class Downloader(ABC):
    @abstractmethod
    async def download(self, symbol: str, start_time: datetime, end_time: datetime, progress_bar: tqdm,
                       interval="1m") -> pd.DataFrame:
        pass


class BinanceDownloader:
    BASE_URL = "https://api.binance.com/api/v3"
    KLINE_ENDPOINT = "/klines"

    def __init__(self, client, rate_limit):
        self.client = client
        self.rate_limit = rate_limit

    @staticmethod
    def to_unix_timestamp(dt: datetime) -> int:
        return int(dt.timestamp() * 1000)

    async def download(self,
                       symbol: str, start_time: datetime, end_time: datetime, progress_bar: tqdm,
                       interval: str) -> pd.DataFrame:
        all_data = []
        current_start = start_time

        while current_start < end_time:
            current_end = min(current_start + timedelta(days=7), end_time)
            params = {
                "symbol": symbol,
                "interval": interval,
                "startTime": self.to_unix_timestamp(current_start),
                "endTime": self.to_unix_timestamp(current_end),
            }

            async with self.rate_limit:
                response = await self.client.get(f"{self.BASE_URL}{self.KLINE_ENDPOINT}", params=params)

                response.raise_for_status()
                data = response.json()

                all_data.extend(data)
                progress_bar.update(len(data))
                current_start = current_end

                df = pd.DataFrame(all_data, columns=[
                    "Open time", "Open", "High", "Low", "Close", "Volume",
                    "Close time", "Quote asset volume", "Number of trades",
                    "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"
                ])
                df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
                return df


async def close(self):
    await self.client.aclose()
