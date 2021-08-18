# App which extend image with text

The app were develop for run as stand-alone app in Mac based OS

## Conditions:

1. Image files have to be placed in the same location where app is.
2. Excel file with information about text, size, color should be placed also in the same location. Excel file headers
   should have following headers:
    1. _Файл с расшеринием_ - file name with this name will be looked for with ".jpg" extension
    2. _Текст_
    3. _Верх/Низ_ - где будет расположен текст
    4. _Центровка текста по горизонтали_ - align
    5. _Сдвиг по вертикали в пикселях_
    6. _Шрифт_ - Название шрифта
    7. _Жирность_ - жирный ли текст
    8. _Доп блоком или нет_ - будет ли добавлен доп блок
    9. _Цвет фона_ - цвет фона если будет вставлен дополнитльный блок
    10. _Размер шрифта_
    11. _Цвет текста_
3. By defualt Arial font will be used which is located in "/System/Library/Fonts/Supplemental/Arial.ttf"
4. Result files will be places in the "result" folder next to app.

## Installation

1. Install dependecies

```bash
python3 -m venv env && source env/bin/activate && pip install -r requirements.txt
```

2. Create a stand-alone executable file

```bash
pyinstaller -F adder.py
```

