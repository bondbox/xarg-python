# coding=utf-8

import os
from typing import Any
from typing import Dict
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

HT = TypeVar("HT")  # head type.
CT = TypeVar("CT")  # cell type.


class form(Generic[HT, CT]):
    """Custom table
    """
    class cell():
        """Cell in the custom table

        Define cells to resolve the null value issue.
        """

        def __init__(self, value: Optional[CT] = None):
            self.value = value

        def __str__(self) -> str:
            return str(self.value if self.value is not None else "")

        @property
        def empty(self) -> bool:
            return self.value is None

        @property
        def value(self) -> Optional[CT]:
            return self.__value

        @value.setter
        def value(self, value: Optional[CT]):
            self.__value = value

    class row():
        """Row in the custom table
        """

        def __init__(self, values: Union[Iterable["form.cell"],
                                         Iterable[Optional[CT]]]):
            self.__cells = [self.new_cell(value=value) for value in values]

        def __len__(self) -> int:
            return len(self.__cells)

        def __iter__(self) -> Iterator["form.cell"]:
            """all cells
            """
            return iter(self.__cells)

        def __getitem__(self, index: int) -> "form.cell":
            return self.__cells[index]

        def __setitem__(self, index: int,
                        value: Union["form.cell",
                                     Optional[CT]]
                        ) -> None:
            self.__cells[index] = self.new_cell(value=value)

        @property
        def values(self) -> Tuple[Optional[CT], ...]:
            """all cell values
            """
            return tuple(cell.value for cell in self)

        def append(self, value: Union["form.cell", Optional[CT]]) -> None:
            self.__cells.append(self.new_cell(value))

        def extend(self, values: Union[Iterable["form.cell"],
                                       Iterable[Optional[CT]]]) -> None:
            self.__cells.extend(self.new_cell(value) for value in values)

        def mapping(self, header: Tuple[HT, ...]) -> Dict[HT, CT]:
            """Map the value of cells into dict
            """
            return {key: cell.value for key, cell in zip(header, self)
                    if cell.value is not None}

        @classmethod
        def new_cell(cls, value: Union["form.cell",
                                       Optional[CT]]
                     ) -> "form.cell":
            return value if isinstance(value, form.cell) else form.cell(value)

    def __init__(self, name: str, header: Iterable[HT] = []):
        self.__rows: List[form.row] = list()
        self.__name: str = name
        self.header = header

    def __len__(self) -> int:
        return len(self.__rows)

    def __iter__(self) -> Iterator["form.row"]:
        """all rows
        """
        return iter(self.__rows)

    def __getitem__(self, index: int) -> "form.row":
        return self.__rows[index]

    def __setitem__(self, index: int,
                    value: Union["form.row",
                                 Iterable["form.cell"],
                                 Iterable[CT]]
                    ) -> None:
        self.__rows[index] = self.new_row(value)

    @property
    def name(self) -> str:
        """table name
        """
        return self.__name

    @property
    def header(self) -> Tuple[HT, ...]:
        """table header (title line)
        """
        return self.__header

    @header.setter
    def header(self, value: Iterable[HT]) -> None:
        self.__header: Tuple[HT, ...] = tuple(i for i in value)

    @property
    def mappings(self) -> Iterator[Dict[HT, CT]]:
        return iter(row.mapping(self.header) for row in self)

    @property
    def values(self) -> Tuple[Tuple[Optional[CT], ...], ...]:
        """all cell values (by row)
        """
        return tuple(row.values for row in self)

    def dump(self) -> Tuple[Tuple[Any, ...], ...]:
        """dump header and all rows
        """
        table: List[Tuple[Any, ...]] = [self.header]
        table.extend(self.values)
        return tuple(table)

    def reflection(self, cells: Dict[HT, CT]) -> "form.row":
        """Re-map the dict to new row object
        """
        return self.new_row(cells=tuple(cells.get(key) for key in self.header))

    def append(self, row: Union["form.row",
                                Iterable["form.cell"],
                                Iterable[CT]]
               ) -> None:
        self.__rows.append(self.new_row(row))

    def extend(self, rows: Iterable[Union["form.row",
                                          Iterable["form.cell"],
                                          Iterable[CT]]]) -> None:
        self.__rows.extend(self.new_row(row) for row in rows)

    @classmethod
    def new_row(cls, cells: Union["form.row",
                                  Iterable["form.cell"],
                                  Iterable[CT]]
                ) -> "form.row":
        return cells if isinstance(cells, form.row) else form.row(values=cells)

    def new_map(self, default: Any = None) -> Dict[HT, Any]:
        """Generate new mapping with default values
        """
        return {key: default for key in self.header}


def tabulate(table: form[Any, Any],
             format: Union[str, TableFormat] = "simple") -> str:
    return __tabulate(tabular_data=table.values,
                      headers=table.header,
                      tablefmt=format)


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
        first: Iterable[str] = sheet.row_values(0)  # first line as header
        table: form[str, Any] = form(name=sheet.name, header=first)
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
            encoding="utf-8", style_compression=0)

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
                value = str(table[row_no][col_no])
                sheet.write(row_no, col_no, value)
                width = wcswidth(value)
                if col_no >= len(widths):
                    sheet.col(col_no).width = self.WIDTH
                    widths.append(0)
                if width > widths[col_no]:
                    sheet.col(col_no).width = self.WIDTH * width
                    widths[col_no] = width

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
        first = [row for row in sheet.iter_rows(max_row=1)][0]
        cells: List[str] = [c.value for c in first if isinstance(c.value, str)]
        table: form[str, Any] = form(name=sheet.title, header=cells)
        for row in sheet.iter_rows(min_row=2):
            table.append([cell.value for cell in row])
        return table

    def load_sheets(self) -> Iterable[form[str, str]]:
        return tuple(self.load_sheet(name) for name in self.book.sheetnames)
