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
    @classmethod
    def run_time(cls, logger=print, show_short_result: int = None):
        """
        :param logger: logger func, default is python print
        :param show_short_result: displays the result of the number of characters.
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                res = func(*args, **kwargs)
                end = time.time()
                logger(
                    f'\n##########################################'
                    f'\nFUNC: {func.__name__}'
                    f'\nSTART: {round(start, 2)} END: {round(end, 2)}'
                    f'\nTOTAL TIME: {round(end - start, 2)}'
                    f'\n##########################################'
                    f'\nRESULT: '+(f'{res}'[:show_short_result]+'......' if show_short_result else f'{res}'))
                return res
            return wrapper
        return decorator

    @classmethod
    def loop_time(cls, loop_times: int = None, loop_sleep: int = 0, logger=print, show_short_result: int = None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                n, flag, start = 1, True, time.time()
                try:
                    (cls.__rangetime(loop_times, n, func, loop_sleep, logger, show_short_result, *args, **kwargs)
                     if loop_times else
                     cls.__whiletime(flag, n, func, loop_sleep, logger, show_short_result, *args, **kwargs))

                except KeyboardInterrupt:
                    pass
                finally:
                    end = time.time()
                    logger(
                        f'\n##########################################'
                        f'\nFUNC: {func.__name__}'
                        f'\nSTART: {round(start, 2)} END: {round(end, 2)}'
                        f'\nTOTAL TIME: {round(end - start, 2)}'
                        f'\n##########################################')
            return wrapper
        return decorator

    @classmethod
    def __rangetime(cls, times, n, func, sleep, logger=print, show_short_result: int = None, *args, **kwargs):
        res = True
        for _ in range(times):
            if res:
                start = time.time()
                res = func(*args, **kwargs)
                end = time.time()
                show_res = f'{res}'[:show_short_result]+'......' if show_short_result else f'{res}'
                logger(f'RESULT: {show_res or "Range loop: Nothing returned."}\n'
                       f'Times: {n}, Time_cost: {end - start}\n')
                time.sleep(sleep)
                n += 1
            else:
                break

    @classmethod
    def __whiletime(cls, flag, n, func, sleep, logger=print, show_short_result: int = None, *args, **kwargs):
        while flag:
            start = time.time()
            res = func(*args, **kwargs)
            end = time.time()
            show_res = f'{res}'[:show_short_result] + '......' if show_short_result else f'{res}'
            logger(f'RESULT: {show_res or "While loop: Nothing returned."}\n'
                   f'Times: {n}, Time_cost: {end - start}\n')
            time.sleep(sleep)
            n += 1
