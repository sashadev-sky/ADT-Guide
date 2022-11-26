from collections.abc import Callable
from timeit import Timer
from typing import Any

def benchmark(funcs: tuple[Callable, ...], values: tuple[tuple[Any, ...]]) -> None:
    """
    Benchmark multiple functions, with, optionally, different values.
    """

    def benchmark_a_func(func: Callable[[Any], Any], values: tuple[Any, ...]) -> None:
        call = f'{func.__name__}({", ".join(str(value) for value in values)})'
        t = Timer(lambda: func(*values)).timeit()
        print(f'{call:40} = {func(*values)} -- {t:.4f} seconds')

    for value in values:
        for func in funcs:
            benchmark_a_func(func, value)
        print()
