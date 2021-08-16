import os
from sys import platform
import collections
from pathlib import Path, PurePath
from string import ascii_letters
import textwrap

from PIL import Image, ImageDraw, ImageFont

MACOS_FONT_PATH = "/System/Library/Fonts/Supplemental/"
MACOS_DEFAULT_FONT_NAME = "Arial.ttf"
RESULT_FOLDER_NAME = "results"
FONT_DEFAULT_COLOR = (0, 0, 0)
FONT_DEFAULT_SIZE = 40
X_MARGIN = 15
Y_MARGIN = 15

ARTICLE_FIELD_NAME = "Файл с расшеринием"
TEXT_FIELD_NAME = "Текст"
UPDOWN_FIELD_NAME = "Верх/Низ"
HOR_ALIGN_FIELD_NAME = "Центровка текста по горизонтали"
VERT_MARGIN_FIELD_NAME = "Сдвиг по вертикали в пикселях"
FONT_NAME_FIELD_NAME = "Шрифт"
BOLD_FIELD_NAME = "Жирность"
ADD_BLOCK_FIELD_NAME = "Доп блоком или нет"
BKGRD_FIELD_NAME = "Цвет фона"
FONT_SIZE_FIELD_NAME = "Размер шрифта"
COLOR_FIELD_NAME = "Цвет текста"

TextParams = collections.namedtuple(
    "TextParams",
    [
        "updown",
        "hor_align",
        "vert_margin",
        "font_name",
        "bold",
        "add_block",
        "bkrg",
        "font_size",
        "color",
    ],
    defaults=[
        1,
        "center",
        Y_MARGIN,
        MACOS_DEFAULT_FONT_NAME,
        False,
        True,
        "white",
        40,
        "black",
    ],
)


class TextAdder:
    def __init__(
        self,
        file_name: str,
        text: str,
        params: TextParams,
        result_path: str = "",
    ):
        self.file_name = file_name
        self.img = Image.open(file_name).convert("RGB")
        self.params = params
        self.result_path = result_path
        font_name = (
            self.params.font_name + " Bold" if params.bold else self.params.font_name
        )
        font_name = os.path.join(MACOS_FONT_PATH, font_name + ".ttf")

        self.font = ImageFont.truetype(
            font_name,
            self.params.font_size,
        )
        self.text = self._get_multiline_text(text, self.font)

    def get_default_font(self) -> str:
        if platform == "darwin":
            return os.path.join(MACOS_FONT_PATH, MACOS_DEFAULT_FONT_NAME)
        elif platform == "win32" or platform == "linux" or platform == "linux2":
            raise OSError("Эта операционная система пока не поддерживается")

    def add_text(self):
        self._draw_text()
        dir_name = Path(self.result_path)
        dir_name.mkdir(mode=0o777, parents=True, exist_ok=True)
        result = PurePath(dir_name, Path(self.file_name).name)
        self.img.save(str(result))

    def _draw_text(self):
        image_editable = ImageDraw.Draw(self.img)

        max_line_size = max([self._get_text_size(x)[0] for x in self.text.split("\n")])

        x = (self.img.size[0] - max_line_size - X_MARGIN) / 2
        y = self.params.vert_margin
        if not self.params.updown:
            text_height = sum(
                [self._get_text_size(x)[1] for x in self.text.split("\n")]
            )
            y = self.img.size[1] - self.params.vert_margin - text_height

        image_editable.multiline_text(
            xy=(x, y),
            text=self.text,
            font=self.font,
            fill=self.params.color,
            align=self.params.hor_align,
        )

    def _add_blank_line(self, height, up: bool = True):

        width, old_height = self.img.size
        new_image = Image.new(
            self.img.mode, (width, old_height + height), self.params.bkrg
        )
        if up:
            new_image.paste(self.img, (0, height))
        else:
            new_image.paste(self.img, (0, 0))
        return new_image

    def _get_multiline_text(self, text, font) -> str:
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(
            ascii_letters
        )  # TODO consider to calc a length for local language
        max_char_count = int((self.img.size[0] - X_MARGIN * 2) * 1.1 / avg_char_width)

        text = textwrap.fill(text=text, width=max_char_count)
        if self.params.add_block:
            _, new_height = self._get_text_size(text)
            self.img = self._add_blank_line(
                new_height * (text.count("\n") + 1), self.params.updown
            )
        return text

    def _get_text_size(self, text):
        size = self.font.getsize(text)
        return size
