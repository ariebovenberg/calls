from typing import Any, Callable, NoReturn, TypeVar

from typing_extensions import Protocol

# Single-sourcing the version number with poetry:
# https://github.com/python-poetry/poetry/pull/2366#issuecomment-652418094
try:
    __version__ = __import__("importlib.metadata").metadata.version(__name__)
except ModuleNotFoundError:  # pragma: no cover
    __version__ = __import__("importlib_metadata").version(__name__)


Q = TypeVar("Q")
R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T", contravariant=True)
U = TypeVar("U", contravariant=True)
V = TypeVar("V", covariant=True)


def raises(__e: BaseException) -> Callable[..., NoReturn]:
    """Create a callable which raises the given exception

    Example
    -------

    >>> f = raises(ValueError("foo"))
    ...
    >>> f()  # any arguments are accepted
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: foo
    """

    def __raises(*_: Any, **__: Any) -> NoReturn:
        raise __e

    return __raises


def const(__v: S) -> Callable[..., S]:
    """Create a callable which always returns the same value

    Example
    -------

    >>> f = const(4)
    ...
    >>> f()  # any arguments are accepted
    4
    """
    return lambda *_, **__: __v


def identity(__v: S) -> S:
    """Pass the given value unmodified

    Example
    -------

    >>> identity(4)
    4
    >>> identity("foo")
    "foo"
    """
    return __v


def flip(__f: "BinaryFunction[Q, R, S]") -> "BinaryFunction[R, Q, S]":
    """Flip the two arguments of a function.
    Often useful in combination with :func:`~functools.partial`.

    Example
    -------

    >>> f = flip(round)
    ...
    >>> f(2, 5.125)
    5.13
    >>> f(0, 3.4)
    3
    """

    def __flipped(__a: R, __b: Q) -> S:
        return __f(__b, __a)

    return __flipped


class UnaryFunction(Protocol[T, V]):
    """A function/callable taking exactly one argument.

    Examples of objects satisfying this protocol:

    >>> # Below are all UnaryFunction[int, float]
    ...
    >>> def myfunc(a: int) -> float:
    ...     return a / 7
    ...
    >>> lambda a: a / 7
    ...
    >>> (7).__rtruediv__
    """

    def __call__(self, __value: T) -> V:
        """ """


class BinaryFunction(Protocol[T, U, V]):
    """A function/callable which takes exactly two arguments."""

    def __call__(self, __a: T, __b: U) -> V:
        """ """
