import pickle

import pytest

from calls import BinaryFunction, always, flip, identity, pipe, raises


def test_raises():
    func = raises(ValueError("foo"))

    with pytest.raises(ValueError, match="foo"):
        func()

    with pytest.raises(ValueError, match="foo"):
        func(8, k=9, self=9)

    with pytest.raises(ValueError, match="foo"):
        pickle.loads(pickle.dumps(func))()

    with pytest.raises(KeyError):
        # mypy checks out
        _: int = raises(KeyError(4))()

    assert repr(func) == f"raises({ValueError('foo')!r})"


def test_always():
    func = always(4)
    assert func("bla") == 4
    assert func(8) == 4
    assert func(8, 4, foo="bla") == 4

    assert pickle.loads(pickle.dumps(always(9)))() == 9

    # mypy checks
    _: float = always(4.5)(foo=5)

    assert repr(always("hi")) == "always('hi')"


def test_identity():
    assert identity(8) == 8
    assert identity(None) is None

    # mypy checks
    _: int = identity(8)


def test_flip():
    flipped = flip(str.center)
    assert flipped(5, "foo") == " foo "
    assert pickle.loads(pickle.dumps(flipped))(5, "foo")

    # mypy checks
    _: BinaryFunction[int, str, str] = flipped

    assert repr(flipped) == "flip(<method 'center' of 'str' objects>)"


def test_pipe():
    obj = object()
    assert pipe()(obj) is obj

    assert pipe(int)("   4 ") == 4

    fn = pipe(str.strip, float, lambda x: int(x * 2), int)
    assert fn("          4.6") == 9

    assert repr(pipe(int, float)) == f"pipe({int!r}, {float!r})"

    assert pickle.loads(pickle.dumps(pipe(float, int)))("3.4") == 3

    def f1(a: str) -> int:
        return int(a)

    def f2(b: int) -> bool:
        return b < 5

    _: bool = pipe(f1, f2)("4")
