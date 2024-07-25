from datetime import datetime
from typing import List

import httpx
import trio
from tqdm import tqdm

from Storage import Storage
from BinanceDownloader import BinanceDownloader, Downloader
from model.DataProcessor import BinanceDefaultProcessor
from model.DataProcessor import DataProcessor


class DataProcessorFactory:
    @staticmethod
    def create(source: str) -> DataProcessor:
        if source == 'Binance':
            return BinanceDefaultProcessor()
        # Add other processors as needed
        raise ValueError(f"Unsupported source: {source}")


class TimeVault:
    def __init__(self, data_dir: str = ""):
        self.client = httpx.AsyncClient()
        self.rate_limit = trio.CapacityLimiter(10)

        self.storage = Storage(data_dir)
        self.apis = {}

    def init(self, source_api: str, api_key: str | None = None):

        if source_api == "Binance":
            self.apis[source_api] = BinanceDownloader(self.client, self.rate_limit)
        # Add other API initializations as needed

    def get_api(self, source_api: str) -> Downloader:
        if source_api not in self.apis:
            raise ValueError(f"API for {source_api} not initialized. Call init() first.")
        return self.apis[source_api]

    async def get_data(self, source: str, symbols: List[str],interval, start_time: datetime, end_time: datetime):
        downloader = self.get_api(source)
        processor = DataProcessorFactory.create(source)
        self.storage.ensure_source_exists(source, symbols)
        async with trio.open_nursery() as nursery:
            for symbol in symbols:
                tmp = self.storage.getParams(source, symbol, start_time, end_time, symbols)
                shouldDownload, newStartTime, newEndTime = tmp

                # print(f" shouldDownload,newStartTime,newEndTime { shouldDownload,newStartTime,newEndTime}")

                if shouldDownload:
                    nursery.start_soon(self._download_and_process,
                                       downloader,
                                       processor,
                                       source,
                                       symbol,
                                       interval,
                                       newStartTime,
                                       newEndTime
                                       )

    async def _download_and_process(self,
                                    downloader: Downloader,
                                    processor: DataProcessor,
                                    source: str,
                                    symbol: str,
                                    interval: str,
                                    start_time: datetime,
                                    end_time: datetime):
        with tqdm(total=None, desc=f"Downloading {symbol} from {source}", unit="B", unit_scale=True,
                  unit_divisor=1024) as progress_bar:
            try:
                df = await downloader.download(symbol, start_time, end_time, progress_bar, interval)
                processed_df = processor.process(symbol,df)
                self.storage.update(source, symbol, start_time, end_time, processed_df)
                print(f"\nSuccessfully downloaded and processed {symbol} from {source}")
            except Exception as e:
                print(f"Error downloading {symbol} from {source}: {str(e)}")
