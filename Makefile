build-windows: 
	pyinstaller.exe -F adder.py

build-osx:
	pyinstaller -F adder.py