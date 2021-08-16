from adder import Adder


def test_data_load():
    adder = Adder(file_name="tests/data/data.xlsx")
    adder.open_file()
    adder.process()
