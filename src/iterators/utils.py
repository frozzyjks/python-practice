from dataclasses import dataclass

_DATABASE = [1, 2, 3, 4, 5, 6, 7, 8, 9]


@dataclass
class Query:
    per_page: int
    page: int


@dataclass
class Response:
    results: list
    total: int


def request(query: Query) -> Response:
    start = (query.page - 1) * query.per_page
    end = start + query.per_page
    results = _DATABASE[start:end]
    return Response(results=results, total=len(_DATABASE))


class Fibo:
    def __init__(self, n: int):
        self.n = n  # сколько чисел нужно вернуть
        self.current = 0  # счётчик — сколько уже вернули
        self.prev = 0  # F(n-2), начинаем с 0
        self.curr = 1  # F(n-1), начинаем с 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.n:
            raise StopIteration

        if self.current == 0:
            result = 0
        elif self.current == 1:
            result = 1
        else:
            new_curr = self.prev + self.curr
            self.prev = self.curr
            self.curr = new_curr
            result = self.curr

        self.current += 1
        return result


class RetrieveRemoteData:
    def __init__(self, per_page: int):
        self.per_page = per_page

    def __iter__(self):
        page = 1
        received = 0

        while True:
            response = request(Query(per_page=self.per_page, page=page))

            for item in response.results:
                yield item
                received += 1

            if received >= response.total:
                break

            page += 1
