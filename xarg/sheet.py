# coding=utf-8

import os
from typing import Any
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union

import openpyxl
from tabulate import TableFormat
from tabulate import tabulate as __tabulate
from wcwidth import wcswidth
import xlrd
import xlwt

KT = TypeVar("KT")  # Title type.
CT = TypeVar("CT")  # Value type.


class form(Generic[KT, CT]):
    """Custom table
    """

    def __init__(self, name: str, title: Iterable[KT]):
        self.__title: Tuple[KT, ...] = tuple(i for i in title)
        self.__datas: List[Tuple[CT, ...]] = list()
        self.__name: str = name

    def __iter__(self) -> Iterator[Tuple[CT, ...]]:
        return iter(self.__datas)

    def __len__(self) -> int:
        return len(self.__datas)

    def __getitem__(self, index: int) -> Tuple[CT, ...]:
        return self.__datas[index]

    @property
    def name(self) -> str:
        """sheet name
        """
        return self.__name

    @property
    def title(self) -> Tuple[KT, ...]:
        """title line
        """
        return self.__title

    def append(self, row: Iterable[CT]) -> None:
        self.__datas.append(tuple(cell for cell in row))


def tabulate(table: form[Any, Any],
             format: Union[str, TableFormat] = "simple") -> str:
    return __tabulate(tabular_data=table, headers=table.title, tablefmt=format)


class xls_reader():
    """Read .xls file
    """

    def __init__(self, filename: str):
        self.__book: xlrd.Book = xlrd.open_workbook(filename)
        self.__file: str = filename

    @property
    def file(self) -> str:
        return self.__file

    @property
    def book(self) -> xlrd.Book:
        return self.__book

    def load_sheet(self, sheet_name: Optional[str] = None) -> form[str, str]:
        sheet_index: int = self.book.sheet_names().index(sheet_name)\
            if isinstance(sheet_name, str) else 0
        sheet: xlrd.sheet.Sheet = self.book.sheet_by_index(sheet_index)
        title: Iterable[str] = sheet.row_values(0)
        table: form[str, Any] = form(name=sheet.name, title=title)
        for i in range(1, sheet.nrows):
            table.append(sheet.row_values(i))
        return table

    def load_sheets(self) -> Iterable[form[str, str]]:
        return tuple(self.load_sheet(name) for name in self.book.sheet_names())


class xls_writer():
    """Write .xls file
    """
    WIDTH = 325

    def __init__(self):
        self.__book: xlwt.Workbook = xlwt.Workbook(
            encoding='utf-8', style_compression=0)

    @property
    def book(self) -> xlwt.Workbook:
        return self.__book

    def save(self, filename: str) -> bool:
        abspath: str = os.path.abspath(filename)
        try:
            dirname: str = os.path.dirname(abspath)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            self.book.save(abspath)
            return True
        except Exception:
            # f"failed to write file {abspath}"
            return False

    def dump_sheet(self, table: form[Any, Any]):
        sheet: xlwt.Worksheet = self.book.add_sheet(
            table.name, cell_overwrite_ok=True)
        widths: List[int] = []
        for row_no in range(len(table)):
            for col_no in range(len(table[row_no])):
                value = table[row_no][col_no]
                sheet.write(row_no, col_no, value)
                awidth = wcswidth(str(value))
                if col_no >= len(widths):
                    sheet.col(col_no).width = self.WIDTH
                    widths.append(0)
                if awidth > widths[col_no]:
                    sheet.col(col_no).width = self.WIDTH * awidth
                    widths[col_no] = awidth

    def dump_sheets(self, tables: Iterable[form[Any, Any]]):
        for table in tables:
            self.dump_sheet(table=table)


class xlsx():
    """Read or write .xlsx file
    """

    def __init__(self, filename: str, read_only: bool = True):
        self.__book: openpyxl.Workbook = openpyxl.load_workbook(
            filename=filename, read_only=read_only)
        self.__file: str = filename

    @property
    def file(self) -> str:
        return self.__file

    @property
    def book(self) -> openpyxl.Workbook:
        return self.__book

    def load_sheet(self, sheet_name: Optional[str] = None) -> form[str, Any]:
        def get_default_sheet_name() -> str:
            if isinstance(sheet_name, str):
                return sheet_name
            active_sheet = self.book.active
            if active_sheet is not None:
                return active_sheet.title
            return self.book.sheetnames[0]

        sheet = self.book[get_default_sheet_name()]
        cells = [row for row in sheet.iter_rows(max_row=1)][0]
        title: List[str] = [c.value for c in cells if isinstance(c.value, str)]
        table: form[str, Any] = form(name=sheet.title, title=title)
        for row in sheet.iter_rows(min_row=2):
            table.append([cell.value for cell in row])
        return table

    def load_sheets(self) -> Iterable[form[str, str]]:
        return tuple(self.load_sheet(name) for name in self.book.sheetnames)