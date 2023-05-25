# Library Logging

## Installation

```sh
pip install git+https://github.com/renaldyresa/logging-gli@main
```

## Configuration

Pada file main.py project tambahkan syntax (syntax ini harus diletakkan pada awal file main.py) berikut:
```python
import os
os.environ["LOG_TYPE"] = "CONSOLE"
os.environ["APP_NAME"] = "TEST-LOGGING"
```

Value LOG_TYPE, yaitu:
- CONSOLE -> untuk log pada console/terminal.
- GCP -> untuk log pada Google cloud platform.
- LOCAL -> untuk log pada file.

Value APP_NAME, yaitu nama dari aplikasi yang di buat.


## Documentation

cara menggunakan library Logging sebagai berikut:

```python
from logging_gli import LoggingGLI, log

# untuk membuat log dengan logger key,
# object logGli akan dipakai terus untuk membuat log dengan 1 alur yg sama
logGli = LoggingGLI()
logGli.info(message="test log info") # log info
logGli.error(message="test log error") # log error
logGli.warning(message="test log warning") # log warning
logGli.debug(message="test log debug") # log debug
logGli.critical(message="test log critical") # log critical

# untuk membuat log tanpa memerlukan logger key
log.info(message="test log info") # log info
log.error(message="test log error") # log error
log.warning(message="test log warning") # log warning
log.debug(message="test log debug") # log debug
log.critical(message="test log critical") # log critical
```
