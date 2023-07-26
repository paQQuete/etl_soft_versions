import os


class Extractor:
    def __init__(self):
        self.files = os.listdir('./data')
        self._json_filter()

    def _json_filter(self):
        self.files = [x for x in self.files if x.split('.')[1] == 'json']

    @property
    def names(self) -> list:
        return self.files
