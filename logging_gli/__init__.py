from .src import LoggingGLI


def __createLog():
    return LoggingGLI(withLogKey=False)


log = __createLog()

__all__ = [
    "LoggingGLI",
    "log"
]
