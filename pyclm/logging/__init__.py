
import os
import sys
import weakref
import time
import traceback

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.struct_pb2 import Struct

import yandexcloud
from yandex.cloud.logging.v1.log_ingestion_service_pb2_grpc import LogIngestionServiceStub
from yandex.cloud.logging.v1.log_ingestion_service_pb2 import WriteRequest
from yandex.cloud.logging.v1.log_entry_pb2 import IncomingLogEntry, Destination, LogLevel
from yandex.cloud.logging.v1.log_resource_pb2 import LogEntryResource

_CLOUD_LOGLEVEL = {
    'LEVEL_UNSPECIFIED': LogLevel.Level.LEVEL_UNSPECIFIED,
    'TRACE': LogLevel.Level.TRACE,
    'DEBUG': LogLevel.Level.DEBUG,
    'INFO': LogLevel.Level.INFO,
    'WARN': LogLevel.Level.WARN,
    'ERROR': LogLevel.Level.ERROR,
    'FATAL': LogLevel.Level.FATAL
}


class Logger:
    def __init__(
            self, sdk: yandexcloud.SDK = None,
            log_group_id: str = None, resource_type: str = None, resource_id: str = None,
            credentials: dict = None, elements: int = 100, period: int = 10
    ):
        if sdk is None:
            sdk = yandexcloud.SDK(**credentials)
        self.service = sdk.client(LogIngestionServiceStub)
        self.group = log_group_id
        self.resource = {
            "type": resource_type or str(os.uname()[1]),
            "id": resource_id or str(os.getpid())
        }
        self.elements = elements if 0 < elements <= 100 else 100
        self.entries = []
        self.period = period
        self.timer = time.time() + self.period
        self._finalizer = weakref.finalize(self, self.write, 0)

    def write(self, c: int = 0):
        if len(self.entries) > c:
            self._write()

    @staticmethod
    def _message(args, kwargs, level='LEVEL_UNSPECIFIED'):
        _timestamp = Timestamp()
        _timestamp.GetCurrentTime()
        result = {
            "level": _CLOUD_LOGLEVEL[level],
            "timestamp": _timestamp,
            "message": "",
            "json_payload": {}
        }
        if len(args) > 0:
            result["message"] = str(args[0])
            result["json_payload"]["messages"] = list(map(str, args))
        if len(kwargs.keys()) > 0:
            if "message" in kwargs:
                result["message"] = str(kwargs["message"])
            result["json_payload"].update(kwargs)
        return result

    def _write(self):
        self.service.Write(WriteRequest(
            destination=Destination(log_group_id=self.group),
            resource=LogEntryResource(**self.resource),
            entries=self.entries
        ))
        self.entries = []
        self.timer = time.time() + self.period

    def _add(self, value: dict):
        payload = Struct()
        try:
            payload.update(value["json_payload"])
        except Exception as e:
            self.error(e)
        else:
            value["json_payload"] = payload
        self.entries.append(IncomingLogEntry(**value))

    def _send(self, value: dict):
        self._add(value)
        if len(self.entries) >= self.elements or self.timer < time.time():
            self._write()

    @staticmethod
    def _extract(stack: traceback.StackSummary):
        result = []
        for frame in stack:
            result.append({
                "filename": frame.filename, "number": frame.lineno, "name": frame.name,
                "line": frame.line, "locals": frame.locals
            })
        return result

    def trace(self, *args, **kwargs):
        message = self._message(args, kwargs, level="TRACE")
        message["json_payload"]["stack"] = self._extract(traceback.extract_stack())
        self._send(message)

    def debug(self, *args, **kwargs):
        self._send(self._message(args, kwargs, level='DEBUG'))

    def info(self, *args, **kwargs):
        self._send(self._message(args, kwargs, level='INFO'))

    def error(self, *args, **kwargs):
        self._send(self._message(args, kwargs, level="ERROR"))

    def fatal(self, *args, **kwargs):
        message = self._message(args, kwargs, level='FATAL')
        _type, _value, _traceback = sys.exc_info()
        if _type is not None:
            message["message"] = str(_value)
            message["json_payload"].update({
                "error": _type.__name__,
                "traceback": self._extract(traceback.extract_tb(_traceback))
            })
            traceback.clear_frames(_traceback)
        self._send(message)

    critical = fatal

    def warn(self, *args, **kwargs):
        self._send(self._message(args, kwargs, level='WARN'))

    warning = warn
