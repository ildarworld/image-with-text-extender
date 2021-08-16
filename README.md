# App which extend image with text

The app were develop for run as stand-alone app in Mac based OS

## Conditions:

1. Image files have to be placed in the same location where app is.
2. Excel file with information about text, size, color should be placed also in the same location. Excel file headers
   should have following headers:
    1. _Артикул_ - file name with this name will be looked for with ".jpg" extension
    2. _Текст_
    3. _Размер текста_
    4. _Цвет_
3. By defualt Arial font will be used which is located in "/System/Library/Fonts/Supplemental/Arial.ttf"
4. Result files will be places in the "result" folder next to app.

## Installation

1. Install dependecies

```bash
python3 -m venv env && source env/bin/activate && pip install -r requirements.txt
```

2. Create stand-alone executable file

```bash
pyinstaller -F adder.py
```

