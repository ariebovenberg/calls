import pytest

from calls import BinaryFunction, const, flip, identity, raises


def test_raises():
    func = raises(ValueError(3))

    with pytest.raises(ValueError, match="3"):
        func()

    with pytest.raises(ValueError, match="3"):
        func(8, k=9)


def test_const():
    func = const(4)
    assert func("bla") == 4
    assert func(8) == 4
    assert func(8, 4, foo="bla") == 4


def test_identity():
    assert identity(8) == 8
    assert identity(None) is None


def test_flip():
    def func(a: int, b: str) -> str:
        return b * a

    flipped: BinaryFunction[str, int, str] = flip(func)
    assert flipped("foo", 3) == "foofoofoo"
