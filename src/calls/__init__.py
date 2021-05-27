from dataclasses import dataclass
from typing import Any, Callable, Tuple, TypeVar, overload

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
V = TypeVar("V", contravariant=True)
W = TypeVar("W", contravariant=True)
X = TypeVar("X", covariant=True)


# We return `Any` here so the result fits anywhere, type-wise.
# Returning `typing.NoReturn` would be technically correct,
# but render the function uncomposable.
def raises(__e: BaseException) -> Callable[..., Any]:
    """Create a callable which raises the given exception.

    The return value is marked :data:`~typing.Any` so its signature
    fits anywhere a callable is needed.

    Example
    -------

    >>> f = raises(ValueError("foo"))
    ...
    >>> f()  # any arguments are accepted
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: foo

    Note
    ----
    The resulting callable is picklable if the given value is.
    """
    return __raises(__e)


@dataclass(frozen=True, repr=False)
class __raises:
    __slots__ = ("_exception",)
    _exception: BaseException

    def __call__(*args: Any, **_: Any) -> Any:
        raise args[0]._exception  # unnamed arg as to not conflict with kwargs

    def __repr__(self) -> str:
        return f"raises({self._exception!r})"

    def __getstate__(self) -> object:
        return self._exception

    def __setstate__(self, s: object) -> None:
        object.__setattr__(self, "_exception", s)


def always(__v: S) -> Callable[..., S]:
    """Create a callable which always returns the same value

    Example
    -------

    >>> f = always(4)
    ...
    >>> f()  # any arguments are accepted
    4

    Note
    ----
    The resulting callable is picklable if the given value is.
    """
    return __always(__v)


@dataclass(frozen=True, repr=False)
class __always:
    __slots__ = ("_value",)
    _value: Any

    def __call__(*args: Any, **_: Any) -> Any:
        return args[0]._value  # unnamed arg as to not conflict with any kwargs

    def __repr__(self) -> str:
        return f"always({self._value!r})"

    def __getstate__(self) -> object:
        return self._value

    def __setstate__(self, s: object) -> None:
        object.__setattr__(self, "_value", s)


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

    Note
    ----
    The resulting callable is picklable if the original is.
    """
    return __flip(__f)


@dataclass(frozen=True, repr=False)
class __flip:
    __slots__ = ("_function",)
    _function: Any

    def __call__(self, __a: Any, __b: Any) -> Any:
        return self._function(__b, __a)

    def __repr__(self) -> str:
        return f"flip({self._function!r})"

    def __getstate__(self) -> object:
        return self._function

    def __setstate__(self, s: object) -> None:
        object.__setattr__(self, "_function", s)


T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
T7 = TypeVar("T7")
T8 = TypeVar("T8")
T9 = TypeVar("T9")


# The copious overloads are to enable mypy to
# deduce the proper callable types -- up to a limit.


@overload
def pipe() -> Callable[[T1], T1]:
    ...


@overload  # noqa: F811
def pipe(__f1: Callable[[T1], T2]) -> Callable[[T1], T2]:
    ...


@overload  # noqa: F811
def pipe(
    __f1: Callable[[T1], T2], __f2: Callable[[T2], T3]
) -> Callable[[T1], T3]:
    ...


@overload  # noqa: F811
def pipe(
    __f1: Callable[[T1], T2],
    __f2: Callable[[T2], T3],
    __f3: Callable[[T3], T4],
) -> Callable[[T1], T4]:
    ...


@overload  # noqa: F811
def pipe(
    __f1: Callable[[T1], T2],
    __f2: Callable[[T2], T3],
    __f3: Callable[[T3], T4],
    __f4: Callable[[T4], T5],
) -> Callable[[T1], T5]:
    ...


@overload  # noqa: F811
def pipe(
    __f1: Callable[[T1], T2],
    __f2: Callable[[T2], T3],
    __f3: Callable[[T3], T4],
    __f4: Callable[[T4], T5],
    __f5: Callable[[T5], T6],
) -> Callable[[T1], T6]:
    ...


@overload  # noqa: F811
def pipe(
    __f1: Callable[[T1], T2],
    __f2: Callable[[T2], T3],
    __f3: Callable[[T3], T4],
    __f4: Callable[[T4], T5],
    __f5: Callable[[T5], T6],
    __f6: Callable[[T6], T7],
) -> Callable[[T1], T7]:
    ...


@overload  # noqa: F811
def pipe(
    __f1: Callable[[T1], T2],
    __f2: Callable[[T2], T3],
    __f3: Callable[[T3], T4],
    __f4: Callable[[T4], T5],
    __f5: Callable[[T5], T6],
    __f6: Callable[[T6], T7],
    __f7: Callable[[T7], T8],
) -> Callable[[T1], T8]:
    ...


@overload  # noqa: F811
def pipe(
    __f1: Callable,
    __f2: Callable,
    __f3: Callable,
    __f4: Callable,
    __f5: Callable,
    __f6: Callable,
    __f7: Callable,
    *__fn: Callable,
) -> Callable:
    ...


def pipe(*__fs: Any) -> Any:  # noqa: F811
    """Create a new callable by piping several in succession

    Example
    -------

    >>> fn = pipe(float, lambda x: x / 4, int)
    >>> fn('9.3')
    9

    Note
    ----
    * Type checking is supported up to 7 functions,
      due to limitations of the Python type system.
    * The resulting callable is picklable if the given callables are.
    """
    return __pipe(__fs)


@dataclass(frozen=True, repr=False)
class __pipe:
    __slots__ = ("_functions",)
    _functions: Tuple[Callable[[Any], Any], ...]

    def __call__(self, value: Any) -> Any:
        for f in self._functions:
            value = f(value)
        return value

    def __repr__(self) -> str:
        return f"pipe{self._functions}"

    def __getstate__(self) -> object:
        return self._functions

    def __setstate__(self, s: object) -> None:
        object.__setattr__(self, "_functions", s)


class UnaryFunction(Protocol[W, X]):
    """:class:`~typing.Protocol` for a callable taking exactly one argument.

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

    def __call__(self, __value: W) -> X:
        """ """


class BinaryFunction(Protocol[V, W, X]):
    """:class:`~typing.Protocol` for a callable which takes exactly two arguments.

    Examples of objects satisfying this protocol:

    >>> # Below are all BinaryFunction[str, int, str]
    ...
    >>> def myfunc(s: str, w: int) -> str:
    ...     return a.center(b)
    ...
    >>> lambda s, w: s.center(w)
    ...
    >>> str.center
    """

    def __call__(self, __a: V, __b: W) -> X:
        """ """
