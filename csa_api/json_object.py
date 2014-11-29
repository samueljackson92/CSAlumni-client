__author__ = "Samuel Jackson"
__date__ = "November 28, 2014"
__license__ = "MIT"

class JSONObject(object):

    def __init__(self, entries={}):
        self.add_entries(entries)

    def __setitem__(self, key, item):
        if key in self.__dict__:
            self.__dict__[key] = item
        else:
            self.add_entries({key: item})

    def __getitem__(self, key):
        return self.__dict__[key]

    def as_json(self):
        return self.__dict__

    def add_entries(self, entries):
        self.__dict__.update(entries)
