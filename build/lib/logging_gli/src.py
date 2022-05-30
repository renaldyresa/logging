import datetime
import os
import time
from abc import ABC, abstractmethod
from google.cloud import logging
from google.cloud.logging_v2.resource import Resource
from .exceptions import TypeLogError, LocalLogDirectoryError

LOG_LOCAL = "LOCAL"
LOG_GCP = "GCP"
LOG_CONSOLE = "CONSOLE"


def decoLogKey(func):

    def wrapper(obj, *args, **kwargs):
        if obj.withLogKey:
            kwargs["logger_key"] = str(time.time()).replace(".", "")
        func(obj, *args, **kwargs)

    return wrapper


class AbstractLogGLI(ABC):

    def __init__(self, appName, withLogKey=True):
        self.appName = appName
        self.withLogKey = withLogKey

    @abstractmethod
    @decoLogKey
    def logStruct(self, severity, **kwargs):
        raise NotImplementedError()


class LoggingGLI:

    def __init__(self, withLogKey=True, pathLocal=None):
        typeLog = os.getenv("LOG_TYPE", LOG_CONSOLE)
        appName = os.getenv("APP_NAME", "")

        if typeLog not in (LOG_LOCAL, LOG_GCP, LOG_CONSOLE):
            raise TypeLogError()

        self.__appName = appName
        self.__typeLog = typeLog
        self.__logger = self.__setLogger(withLogKey, pathLocal)

    def __setLogger(self, withLogKey, pathLocal) -> AbstractLogGLI:
        if self.__typeLog == LOG_LOCAL:
            return LogLocal(self.__appName, withLogKey, pathLocal)
        elif self.__typeLog == LOG_CONSOLE:
            return LogConsole(self.__appName, withLogKey)
        elif self.__typeLog == LOG_GCP:
            return LogGCP(self.__appName, withLogKey)
        else:
            raise TypeLogError()

    def info(self, **kwargs):
        self.__logger.logStruct(severity="INFO", **kwargs)

    def debug(self, **kwargs):
        self.__logger.logStruct(severity="DEBUG", **kwargs)

    def warning(self, **kwargs):
        self.__logger.logStruct(severity="WARNING", **kwargs)

    def error(self, **kwargs):
        self.__logger.logStruct(severity="ERROR", **kwargs)

    def critical(self, **kwargs):
        self.__logger.logStruct(severity="CRITICAL", **kwargs)


class LogLocal(AbstractLogGLI):

    def __init__(self, appName, withLogKey, pathLocal):
        super().__init__(appName, withLogKey)
        if appName in ("", None):
            raise LocalLogDirectoryError()

        self.__path = f"./log_{appName}" if pathLocal is None else pathLocal
        self.__filename = f'{datetime.datetime.now().strftime("%Y-%m-%d")}.txt'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)

    @decoLogKey
    def logStruct(self, severity, **kwargs):
        with open(f"{self.__path}/{self.__filename}", "a+") as f:
            f.write(f"{severity}: {kwargs}")


class LogConsole(AbstractLogGLI):

    @decoLogKey
    def logStruct(self, severity, **kwargs):
        print(f"{severity}: {kwargs}")


class LogGCP(AbstractLogGLI):

    def __init__(self, appName, withLogKey):
        super().__init__(appName, withLogKey)
        self.__client = logging.Client()
        self.__tLogger = self.__client.logger(self.appName)
        self.__resource = Resource(
            type="gae_app",
            labels={
                "module_id": os.environ.get("GAE_SERVICE"),
                "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT"),
                "version_id": os.environ.get("GAE_VERSION")
            }
        )

    @decoLogKey
    def logStruct(self, severity, **kwargs):
        self.__tLogger.log_struct(info=kwargs, severity=severity, resource=self.__resource)

