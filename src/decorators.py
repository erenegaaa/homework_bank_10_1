from functools import wraps
from typing import Callable, Any, Optional
import sys


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для логирования выполнения функций.
    Если указан filename, логи записываются в файл.
    Иначе выводятся в консоль.
    """


    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok\n"
            except Exception as e:
                message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(message)
                else:
                    print(message, file=sys.stdout, end="")
                raise

            if filename:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(message)
            else:
                print(message, file=sys.stdout, end="")
            return result

        return wrapper


    return decorator
