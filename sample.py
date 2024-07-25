import trio
import httpx
from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm
import nasdaqdatalink
from abc import ABC, abstractmethod
from typing import List, Dict, Any,NamedTuple
import os
import yaml
from typing import TypedDict,List
import json
import os.path
from pydantic import BaseModel, ValidationError
import pickle


from model.DataProcessor import DataProcessor,BinanceDefaultProcessor
from TimeVault import TimeVault


async def main():
    vault = TimeVault("./")
    symbols = ["BTCUSDT", "ETHUSDT"]

    vault.init("Binance")

    start_date = datetime(2024, 6, 6)
    end_date = datetime.now()

    await vault.get_data("Binance", symbols,'1m', start_date, end_date)


async def main2():
    vault = TimeVault("./")
    symbols = ["BTCUSDT", "ETHUSDT"]

    vault.init("Binance")

    start_date = datetime(2023, 1, 1)
    end_date = datetime.now()

    await vault.get_data("Binance", symbols,'1m', start_date, end_date)
trio.run(main)