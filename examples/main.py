
import os
import subprocess
from pyclm.logging import Logger


def test_warn(log: Logger):
    log.warning("warning logger message", "А", "A", 0, 1, 0.123, None)


def test_info(log: Logger):
    log.info("Info with attr", any_list=["А", "A", 0, 1, 0.123, None])


def test_debug(log: Logger):
    log.debug(
        "Debug log message", any_json={"ch_ru": "Яндекс", "ch_en": "Yandex", "cloud": {"logging": 5, "service": 0}}
    )


def test_error(log: Logger):
    log.error("Error log message A")


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
        credentials={"token": os.environ.get("TOKEN")}, elements=50
    )
    test_warn(_logger)
    test_info(_logger)
    test_error(_logger)
    test_debug(_logger)
    test_critical(_logger)
    test_trace(_logger)