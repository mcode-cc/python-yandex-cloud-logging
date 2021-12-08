
import os
import time

from pyclm.logging import Logger


def test_warn(log: Logger):
    log.warning("warning logger message", "А", "B", 0, 1, 0.123, None)


def test_info(log: Logger):
    log.info("Info with attr", any_list=["А", "B", 0, 1, 0.123, None])


def test_debug(log: Logger):
    log.debug(
        "Debug log message", any_json={"ch_ru": "Яндекс", "ch_en": "Yandex", "cloud": {"logging": 5, "service": 0}}
    )


def test_error(log: Logger):
    log.error("Error log message")


def test_trace(log: Logger):
    log.trace("Trace with stack")


def test_critical(log: Logger):
    try:
        raise Exception("Real Exc")
    except Exception as e:
        log.fatal(e)
    log.fatal("Fatal without try/except")


if __name__ == '__main__':

    _logger = Logger(
        log_group_id=os.environ.get("LOG_GROUP_ID"),
        credentials={"token": os.environ.get("TOKEN")}
    )

    _ptns = time.process_time_ns()
    _tns = time.time_ns()

    for _ in range(100):
        test_warn(_logger)
        test_info(_logger)
        test_error(_logger)
        test_debug(_logger)
        test_critical(_logger)
        test_trace(_logger)
    print((time.process_time_ns() - _ptns)/10**9, (time.time_ns() - _tns)/10**9)

    # 0.122077 0.758518  elements=100, period = 10, workers = 0 (default)
    # 1.05552 65.05855 elements=1, period = 10, workers = 0
    # ~ 0.045114 0.043375 elements=100, period = 10, workers = 1 with multiprocessing

