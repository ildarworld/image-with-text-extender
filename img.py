import math
from sys import platform
from pathlib import Path, PurePath
from string import ascii_letters
import textwrap

from PIL import Image, ImageDraw, ImageFont

MACOS_DEFAULT_FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
RESULT_FOLDER_NAME = "results"
FONT_DEFAULT_COLOR = (0, 0, 0)
FONT_DEFAULT_SIZE = 40
X_MARGIN = 15
Y_MARGIN = 15


class TextAdder:
    def __init__(
        self,
        file_name: str,
        result_path: str = "",
        text: str = "",
        font_size: int = FONT_DEFAULT_SIZE,
        font_name: str = None,
        font_color: tuple = FONT_DEFAULT_COLOR,
        up: bool = True,
    ):
        self.file_name = file_name
        self.img = Image.open(file_name).convert("RGB")

        self.font_size = font_size
        self.result_path = result_path
        self.bg_color = font_color
        self.up = up or True

        self.font_name = font_name or self.get_default_font()
        print("Font name", self.font_name)
        self.font = ImageFont.truetype(self.font_name, font_size)
        self.text = self._get_multiline_text(text, self.font)

    def get_default_font(self) -> str:
        if platform == "darwin":
            return MACOS_DEFAULT_FONT_PATH
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

        image_editable.multiline_text(
            xy=(x, 0),
            text=self.text,
            font=self.font,
            fill=self.bg_color,
            align="center",
        )

    def _add_blank_line(self, height):

        width, old_height = self.img.size

        mode = self.img.mode
        if len(mode) == 1:  # L, 1
            new_background = 255
        if len(mode) == 3:  # RGB
            new_background = (255, 255, 255)
        if len(mode) == 4:  # RGBA, CMYK
            new_background = (255, 255, 255, 255)

        new_image = Image.new(mode, (width, old_height + height), new_background)

        new_image.paste(self.img, (0, height))
        return new_image

    def _get_multiline_text(self, text, font) -> str:
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(
            ascii_letters
        )  # TODO consider to calc a length for local language
        max_char_count = int((self.img.size[0] - X_MARGIN * 2) * 1.1 / avg_char_width)

        text = textwrap.fill(text=text, width=max_char_count)
        _, new_height = self._get_text_size(text)
        self.img = self._add_blank_line(new_height * (text.count("\n") + 1))

        return text

    def _get_text_size(self, text):
        size = self.font.getsize(text)
        return size
