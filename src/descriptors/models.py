class Field:
    def __init__(self, path: str):
        self.path = path
        self.keys = path.split(".")

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        data = obj.payload
        for key in self.keys:
            if not isinstance(data, dict) or key not in data:
                return None
            data = data[key]

        return data

    def __set__(self, obj, value):
        data = obj.payload

        for key in self.keys[:-1]:
            data = data[key]

        data[self.keys[-1]] = value


class Model:
    def __init__(self, payload: dict):
        self.payload = payload
