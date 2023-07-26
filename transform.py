import datetime
import json
import codecs
import traceback

from typing import List, Union


def patch_date(data: List[dict]) -> Union[List[dict], bool]:
    for row in data:
        if type(row) == list:
            return None
        if row['InstallDate']:
            row['InstallDate'] = datetime.date(
                year=int(row['InstallDate'][0:4]),
                month=int(row['InstallDate'][4:6]),
                day=int(row['InstallDate'][-2:])
            )
    return data


def validate_dicts(data: List[dict]) -> List[dict]:
    k = ('Publisher', 'DisplayName', 'DisplayVersion', 'InstallDate')
    new_data = list()
    for row in data:
        if tuple(row.keys()) == k:
            new_data.append(row)
    return new_data


def escape_values(data: List[dict]) -> List[dict]:
    new_data = []
    for row in data:
        for key, value in row.items():
            if value:
                escaped_query = str(value).replace("\u0000", "").replace("'", "''").replace('"', '\\"')
                row[key] = escaped_query
        new_data.append(row)
        
    return new_data


class ResponseObject:
    def __init__(self, filename: str):
        '''
        :param filename: name of file with extension
        '''
        self.filename = filename
        self._data = self._make_data()

    def _make_data(self):
        with codecs.open(f'./data/{self.filename}', encoding='utf-8-sig') as file:
            data = json.load(file)
        data = validate_dicts(data)
        data = patch_date(data)
        data = escape_values(data)
        return data

    @property
    def data(self) -> List[dict]:
        return self._data

    @property
    def hostname(self) -> str:
        return self.filename.split('~')[0]

    @property
    def username(self) -> str:
        return self.filename.split('~')[1]

    @property
    def timestamp(self) -> str:
        return self.filename.split('~')[2].split(',')[0]