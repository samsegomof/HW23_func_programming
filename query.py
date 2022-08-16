from flask import abort
from itertools import islice

from constants import COMMANDS


class Query:
    def __init__(self, file_name, cmd1: str, value1: str, cmd2: str | None, value2: str | None):
        self.data = self.read_data(file_name)

        if cmd1 is None or cmd1 not in COMMANDS:
            abort(400, 'Передайте команду или проверьте что она есть в перечне команд')
        self.cmd1 = cmd1
        self.value1 = value1

        if cmd2 and cmd2 not in COMMANDS:
            abort(400)
        self.cmd2 = cmd2
        self.value2 = value2

    @staticmethod
    def read_data(file_name: str):
        """Чтение лог-файла"""
        with open(file_name, 'r') as f:
            while True:
                try:
                    yield next(f)
                except StopIteration:
                    break

    def implement_request(self):
        """
        Реализация запроса
        """
        queries = {'filter': self.filter_,
                   'map': self.map_,
                   'sort': self.sort_,
                   'limit': self.limit_,
                   'unique': self.unique_
                   }
        queries[self.cmd1](self.value1)

        if self.cmd2:
            queries[self.cmd2](self.value2)

        return self.data

    def filter_(self, string_to_search: str) -> None:
        """Фильтр данных по запросу"""
        self.data = filter(lambda x: string_to_search in x, self.data)

    def map_(self, column: int) -> None:
        """Изменение формата данных"""
        try:
            column = int(column)
        except ValueError:
            abort(400)

        if column > 2:
            abort(400)
        self.data = map(lambda x: x.replace(' - - [', ' '), self.data)
        self.data = map(lambda x: x.replace(' +0000]', ' '), self.data)
        self.data = map(lambda x: x.split(' ', maxsplit=2)[column] + '/n', self.data)

    def sort_(self, sort_type: str) -> None:
        """Сортировка данных по возрастанию или убыванию
        :param sort_type: asc или desc
        """
        if sort_type not in ['asc', 'desc']:
            abort(400)

        sort_type = True if sort_type == 'desc' else False
        self.data = sorted(self.data, reverse=sort_type)

    def limit_(self, count: int) -> None:
        """Получение запрашиваемого количества из строки"""
        try:
            count = int(count)
        except ValueError:
            abort(400)

        self.data = islice(self.data, count)

    def unique_(self):
        """Получение уникальных значений"""
        self.data = iter(set(self.data))
