import os
from openpyxl import load_workbook

import consts
from img import TextAdder

ARTICLE_FIELD_NAME = "Артикул"
TEXT_FIELD_NAME = "Текст"
TEXT_SIZE_FIELD_NAME = "Размер текста"
COLOR_FIELD_NAME = "Цвет"

COLORS_SCHEME = {
    "черный": "black",
    "белый": "white",
    "серый": "gray",
    "красный": "red",
}

XLSX_HEADERS = {
    ARTICLE_FIELD_NAME,
    TEXT_FIELD_NAME,
    TEXT_SIZE_FIELD_NAME,
    COLOR_FIELD_NAME,
}


class Adder:
    def __init__(self, file_name: str = None):
        self.file_name = file_name
        self._items = []
        self._path_name, _ = os.path.split(file_name)
        self._work_sheet = None
        self._file_headers: dict = dict()

    def open_file(self):
        work_book = load_workbook(self.file_name, read_only=True, data_only=True)
        self._work_sheet = work_book.active
        self._file_headers = self._get_headers()
        if not self._file_headers or not XLSX_HEADERS.issubset(self._file_headers):
            print(consts.FILE_OPEN_EXCEPTION_MSG)
            raise ValueError(consts.FILE_OPEN_EXCEPTION_MSG)
        self._read_data()

    def _get_headers(self) -> dict:
        headers = {}
        header_row = next(self._work_sheet.iter_rows(min_row=1, max_col=30))
        for header_number, header in enumerate(header_row):
            headers[header.value] = header_number
        return headers

    def _read_data(self):

        for i, row in enumerate(
            self._work_sheet.iter_rows(min_row=2, max_col=30), start=1
        ):
            img_fn = os.path.join(
                self._path_name,
                str(row[self._file_headers[ARTICLE_FIELD_NAME]].value) + ".jpg",
            )
            result_path = os.path.join(self._path_name, "results")

            text = row[self._file_headers[TEXT_FIELD_NAME]].value
            font_size = row[self._file_headers[TEXT_SIZE_FIELD_NAME]].value
            color = COLORS_SCHEME[row[self._file_headers[COLOR_FIELD_NAME]].value]
            try:
                self._items.append(
                    TextAdder(
                        file_name=img_fn,
                        result_path=result_path,
                        text=text,
                        font_size=font_size,
                        font_color=color,
                    )
                )
            except FileNotFoundError:
                print(f"Не удалось обрабоать строку {i}. Файл {img_fn} не найден")

    def process(self):
        for img in self._items:
            img.add_text()


if __name__ == "__main__":
    import sys

    path_name, _ = os.path.split(sys.argv[0])
    filename = os.path.join(path_name, "images.xlsx")

    frozen = "not"
    if getattr(sys, "frozen", False):
        # we are running in a bundle
        frozen = "ever so"
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    adder = Adder(file_name=filename)
    adder.open_file()
    adder.process()
