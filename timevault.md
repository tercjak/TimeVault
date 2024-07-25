# Timevault : Comprehensive Market Data Solution for Binance,Alpaca,Crypto,Stocks,Futures and more

**Meta Description:** Timevault is a Python-based tool for efficiently downloading, processing, and storing market data from multiple sources like Binance and Alpaca. It features data persistence, partial downloads, and customizable data processing.
## Efficient Market Data Pipeline: Timevault

This document provides an overview of the Timevault, which downloads market data from multiple sources (like Binance,Alpaca), processes it, and stores the results.
## Core Features
* **Data Persistence:** Ensures data integrity with alternating CSV files.
* **Partial Downloads:** Optimizes efficiency by downloading only new data.
* **Flexible Data Processing:** Customizable data processing pipeline.
* **Scalable Architecture:** Handles multiple data sources and concurrent downloads.


## Components
* **Binance API:** Downloads historical kline data from Binance.
* **Data Processors:** Transforms raw data into desired format.
* **Storage:** Persists processed data in CSV format.
* **Vault:** Orchestrates the entire data pipeline.

##Usage



- `init(sourceApi:str,apiKey:str)`: Initialise specific API eg.  

Prepare the parameters for Binance data:
   ```python
async def main():
    vault = TimeVault("./")
    symbols = ["BTCUSDT", "ETHUSDT"]

    vault.init("Binance")

    start_date = datetime(2024, 6, 6)
    end_date = datetime.now()

    await vault.get_data("Binance", symbols,'1m', start_date, end_date)

trio.run(main)
    ```


### DataProcesors

`DataProcessorFactory`: Creates Dataprocessor 

- `create(srcColumns,destColumns) -> DataProcessor]`: creates `Dataprocessor`

`DataProcessor`: Process dataframe
- `process(srcColumns,destColumns) -> DataFrame]`: processes the dataframe, so that only destColumns are returned

DefaultBinance processor saves df in Binance_BTCUSDT_1.csv 

`ds,BTCUSDT
2024-06-05 22:00:00,71138.43000000
2024-06-05 22:01:00,71122.82000000
2024-06-05 22:02:00,71122.23000000
2024-06-05 22:03:00,71215.26000000`


## Core Dependencies

- trio
- httpx

## Future Improvements
- Support for more API endpoints
- Add partial download functionality 
- Add unit and integration tests
- Implement a concrete storage backend(Arrow or Feather)

