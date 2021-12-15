import functools
import time


class Retry:
    @classmethod
    def trying(cls, retry_times: int = 3, retry_sleep: int = 0, retry_exceptions: tuple = None, logger=print):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except (retry_exceptions or Exception) as e:
                    return cls.__retry(func, retry_times, e, retry_sleep, logger, *args, **kwargs)
            return wrapper
        return decorator

    @classmethod
    def __retry(cls, func, retry_times, error, retry_sleep, logger, *args, **kwargs):
        if retry_times >= 1:
            try:
                retry_times -= 1
                logger(f'Retry remaining times: {retry_times}; Will sleep {retry_sleep}s; Error: {error};')
                time.sleep(retry_sleep)
                return func(*args, **kwargs)
            except Exception as e:
                return cls.__retry(func, retry_times, e, retry_sleep, logger, *args, **kwargs)
        else:
            raise


class RunTime:
    pass
