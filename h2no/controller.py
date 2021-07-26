import requests
import datetime
import pandas as pd


class Client:

    def __init__(self, host, password):
        self._host = host
        self._password = password

    def get_station_names(self):
        return self._http_request('jn')['snames']

    def get_logs(self, days):
        station_names = self.get_station_names()

        raw_records = self._http_request('jl', f'hist={days}')
        filtered_raw_records = []

        # ignore ad hoc
        for raw_record in raw_records:
            if raw_record[0] == 99:
                continue

            filtered_raw_records.append(raw_record)

        raw_records = filtered_raw_records

        logs_dataframe = pd.DataFrame(columns=[
            'station_name',
            'liters',
            'liters_per_minute',
            'duration_seconds',
            'start_time',
            'end_time'
        ], index=range(len(raw_records)))

        for raw_record_index, raw_record in enumerate(raw_records):

            station_name = station_names[raw_record[1]]
            duration_seconds = raw_record[2]
            start_time = datetime.datetime.fromtimestamp(raw_record[3] - duration_seconds)
            end_time = datetime.datetime.fromtimestamp(raw_record[3])
            flow_sensor_ticks_per_minute = raw_record[4]

            logs_dataframe.loc[raw_record_index] = {
                'station_name': station_name,
                'liters': 10.0 * flow_sensor_ticks_per_minute * duration_seconds / 60.0,
                'liters_per_minute': 10 * flow_sensor_ticks_per_minute,
                'duration_seconds': duration_seconds,
                'start_time': start_time,
                'end_time': end_time,
            }

        return logs_dataframe

    def _http_request(self, path, params=None):
        url = f'{self._host}/{path}?pw={self._password}'
        if params:
            url += f'&{params}'

        response = requests.get(url)
        response.raise_for_status()

        return response.json()
