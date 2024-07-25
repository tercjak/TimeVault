import datetime
import os
import pickle

import pandas as pd

from model.TrackingConf import TrackingData, TrackingConf, Daterange


class Storage():
    def __init__(self, data_dir: str):
        self.trackingConf = None
        self.data_dir = data_dir
        self.tracking_file = f"{data_dir}/download_tracking.data"

        self._ensure_tracking_file_exists()

    def getParams(self, source, symbol, start_time: datetime, end_time: datetime, symbols) -> tuple[
        bool, datetime, datetime]:
        trackingData = self.trackingConf
        # print(f"trackingData {trackingData}")

        # return True,start_time,end_time
        self.ensure_source_exists(source, symbols)
        
        return True, start_time, end_time

        if trackingData is None:
            srcDict = {}
            srcDict[symbol] = None

            trackingData = TrackingConf()

            trackingData.dictionary[source] = srcDict
            # print(f"newTrackingData {trackingData}")

            self.ensure_source_exists(source, symbols)

            self.trackingConf = trackingData

        if source not in self.trackingConf.dictionary[source]:
            # print("source not in self.trackingConf.dictionary[source]") #<--here
            return True, start_time, end_time
        if symbol not in self.trackingConf.dictionary[source][symbol]:  # .sources
            # print("symbol not in self.trackingConf.dictionary[source][symbol]]")

            return True, start_time, end_time

        t = self.trackingConf.dictionary[source][symbol]  # .sources
        prv_start_time = t.fromDate
        prv_end_time = t.endDate

        prv_start_time = datetime.fromisoformat(prv_start_time)
        prv_end_time = datetime.fromisoformat(prv_end_time)

        if start_time > prv_end_time:
            # print("start_time > prv_end_time")
            return True, prv_end_time, end_time
        elif end_time < prv_start_time:
            # print("end_time < prv_start_time")
            return True, start_time, prv_start_time
        elif end_time > end_time or start_time < prv_start_time:
            # print("end_time > end_time or start_time < prv_start_time")
            return True, start_time, end_time
        else:
            # print("getParams False")
            return False, start_time, end_time

    def _ensure_tracking_file_exists(self):
        # ... (unchanged) ...

        if not os.path.exists(self.tracking_file) or not os.path.isfile(self.tracking_file):
            emptyTrackingData = TrackingConf()
            self.trackingConf = emptyTrackingData
            with open(self.tracking_file, 'wb') as f:
                pickle.dump(emptyTrackingData, f)

        else:
            self.trackingConf = self._load_tracking_data()

    # def _ensure_tracking_file_exists(self):
    #     print("_ensure_tracking_file_exists")
    #     print(f"os.path.isfile(self.tracking_file) {os.path.isfile(self.tracking_file) }")

    #     if not ( os.path.exists(self.tracking_file) )or not (os.path.isfile(self.tracking_file)) :
    #         print(f"not file {self.tracking_file}")
    #         emptyTrackingData=TrackingConf()
    #         self.trackingConf=emptyTrackingData
    #         print(f"emptyTrackingData {emptyTrackingData}")
    #         p2 = emptyTrackingData.model_dump_json(indent=2)

    #         with open(self.tracking_file, 'w') as f:
    #             json.dump(p2, f)

    #     self.trackingConf=self._load_tracking_data()
    #     print("now self.trackingData exist")

    def ensure_source_exists(self, source, symbols):
        print(f"ensure_source_exists")

        trackingData = self.trackingConf
        print(f"_ensure_source_exists tracking_data {trackingData}")

        if trackingData is None:

            srcDict = {}
            for symbol in symbols:
                srcDict[symbol] = None

            trackingData = TrackingConf()

            trackingData.dictionary[source] = srcDict
            self.trackingConf = trackingData

        elif source not in trackingData:

            srcDict = {}
            for symbol in symbols:
                srcDict[symbol] = None

            trackingData.dictionary[source] = srcDict  # .sources

            self.trackingConf = trackingData
            print(f"_ensure_source_exists self.trackingData {self.trackingConf}")
        elif trackingData is not None:
            srcDict = trackingData.dictionary[source]  # .sources

            for symbol in symbols:
                if symbol not in trackingData.dictionary[source]:
                    srcDict[symbol] = None

            trackingData.dictionary[source] = srcDict
            self.trackingConf = trackingData

        self._save_tracking_data(trackingData)

    # def _load_tracking_data(self) -> TrackingConf:
    #     print("_load_tracking_data")

    #     with open(self.tracking_file, 'r') as f:
    #         data = json.load(f)
    #         try:
    #             trackingData = TrackingConf.parse_raw(data)
    #             self.trackingConf=trackingData
    #             print(f"_load_tracking_data {trackingData}")

    #             return trackingData
    #         except ValidationError as exc:
    #             print(repr(exc.errors()[0]['type']))

    #     if not os.path.exists(self.tracking_file) or not os.path.isfile(self.tracking_file) :
    #         print(f"not file {self.tracking_file}")
    #         emptyTrackingData=TrackingConf()
    #         self.trackingConf=emptyTrackingData
    #         print(f"emptyTrackingData {emptyTrackingData}")
    #         p2 = emptyTrackingData.model_dump_json(indent=2)

    #         with open(self.tracking_file, 'w') as f:
    #             json.dump(p2, f)

    #         return self.trackingConf

    def _load_tracking_data(self) -> TrackingConf:
        if not os.path.exists(self.tracking_file) or os.path.getsize(self.tracking_file) == 0:
            return TrackingData(sources={}, total=False)

        with open(self.tracking_file, 'rb') as f:
            return pickle.load(f)

    def _save_tracking_data(self, data: TrackingConf):
        with open(self.tracking_file, 'wb') as f:
            pickle.dump(data, f)

    # def _save_tracking_data(self, data: TrackingConf):
    #     print(f'_save_tracking_data data {data}')
    #     p2 = data.model_dump_json(indent=2)
    #     # print(f'_save_tracking_data p2 {p2}')

    #     # with open(self.tracking_file, "w") as f:
    #     #     json.dump(p2, f, indent=2)

    #     with open(self.tracking_file, "w") as f:
    #         json.dump(p2, f, indent=2)

    def update(self, source: str, symbol: str, start_time: datetime, end_time: datetime, df: pd.DataFrame):
        filename1 = f"{self.data_dir}/{source}_{symbol}_1.csv"
        filename2 = f"{self.data_dir}/{source}_{symbol}_2.csv"

        existing_df = self._load_existing_data(source, symbol)
        merged_df = pd.concat([existing_df, df]).drop_duplicates().sort_values('ds')

        # Alternate between two files to avoid data loss in case of failure
        if os.path.exists(filename1):
            merged_df.to_csv(filename2, index=False)
            os.remove(filename1)
        else:
            merged_df.to_csv(filename1, index=False)
            if os.path.exists(filename2):
                os.remove(filename2)

        self._update_tracking(source, symbol, start_time, end_time)

    def _load_existing_data(self, source: str, symbol: str) -> pd.DataFrame:
        filename1 = f"{self.data_dir}/{source}_{symbol}_1.csv"
        filename2 = f"{self.data_dir}/{source}_{symbol}_2.csv"

        if os.path.exists(filename1):
            return pd.read_csv(filename1)
        elif os.path.exists(filename2):
            return pd.read_csv(filename2)
        return pd.DataFrame()

    def _update_tracking(self, source: str, symbol: str, start_time: datetime, end_time: datetime):
        trackingData = self.trackingConf
        print(f'_update_tracking loaded  {trackingData}')

        # if source not in trackingData['sources']:
        #     trackingData['sources'][source] = SourceData(symbols)
        #     self.trackingData=trackingData
        #     print(f"_update_tracking self.trackingData {self.trackingData}")

        timerange = Daterange(start_time.isoformat(), end_time.isoformat())

        print(f'timerange {timerange} symbol {symbol}')

        trackingData.dictionary[source][symbol] = timerange  # sources
        self.trackingConf = trackingData

        print(f'_update_tracking {trackingData}')

        self._save_tracking_data(trackingData)
