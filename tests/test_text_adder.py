import pytest
from img import TextAdder, TextParams


@pytest.fixture
def params():
    return TextParams(
        updown=True,
        hor_align="center",
        vert_margin=20,
        font_name="Arial",
        bold=True,
        add_block=True,
        bkrg="green",
        font_size=40,
        color="black",
    )


def test_add_text(params):
    path = "tests/data/test.png"
    a = TextAdder(
        file_name=path,
        text="Хвала безумцам, одиночкам, бунтарям, белым воронам, тем кто всегда некстати и невпопад, тем кто видит мир иначе. Они не соблюдают правил, они смеются над устоями, их можно цитировать, спорить с ними, восхвалять или проклинать их, но только игнорировать их - невозможно.",
        params=params,
    )
    a.add_text()
