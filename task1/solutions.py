import inspect
from functools import wraps


def strict(func):
    sig = inspect.signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        for name, value in bound_args.arguments.items():
            expected_type = annotations.get(name)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(
                    f"Аргемент '{name}' должен быть '{expected_type.__name__}', "
                    f"а не '{type(value).__name__}'"
                )

        return func(*args, **kwargs)
    return wrapper
