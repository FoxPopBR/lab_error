
# CustomLogger - A Flexible Logging Utility for Python Projects

## Description

**CustomLogger** is a robust Python logging utility designed to simplify logging management in your projects. This class provides seamless integration for logging messages to both the console and log files, ensuring consistency across outputs. It is built on Python's `logging` module and supports advanced features such as rotating log files, customizable log levels, and detailed error tracking with formatted traceback.

Whether you're building small scripts or large-scale applications, **CustomLogger** offers a simple yet powerful interface to manage your logs effectively.

---

## Features

- **Dual Output**: Logs messages to both console and file with consistent formatting.
- **Rotating File Logs**: Automatically manages log file size with rotation (`maxBytes` and `backupCount`).
- **Customizable Log Levels**: Supports all standard logging levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
- **Traceback Integration**: Logs detailed error tracebacks, optionally excluding the logger's file for cleaner output.
- **Exception Decorator**: Automatically logs exceptions raised within decorated functions.
- **Customizable Options**:
  - Choose log file name and location.
  - Enable or disable console and file logging independently.
  - Include or exclude the logger file from error tracebacks.
- **Thread-Safe**: Built on Python's thread-safe `logging` infrastructure.

---

## Installation

Clone or download the repository and integrate the `CustomLogger` class into your project. No additional dependencies are required beyond Python's standard library.

```bash
git clone https://github.com/your-username/your-repository.git
```

---

## Usage

### Initialization

Instantiate the `CustomLogger` class in your project:

```python
from modules.logger import CustomLogger

logger = CustomLogger(
    name='MyLogger',
    log_file='app.log',
    level=logging.DEBUG,
    console_log=True,
    file_log=True,
    include_logger_in_traceback=False
)
```

### Logging Methods

- **`log_debug(msg)`**: Logs debug messages.
- **`log_info(msg)`**: Logs informational messages.
- **`log_warning(msg)`**: Logs warning messages.
- **`log_error(msg)`**: Logs error messages.
- **`log_critical(msg)`**: Logs critical messages.

```python
logger.log_info("This is an info message.")
logger.log_error("This is an error message.")
```

### Logging Exceptions

Use the `log_exception` decorator to automatically capture and log exceptions:

```python
@logger.log_exception
def my_function():
    raise ValueError("Something went wrong!")

try:
    my_function()
except Exception:
    pass
```

### Default Logger

The module includes a pre-configured default logger:

```python
from modules.logger import default_logger

default_logger.log_info("Using the default logger!")
```

---

## Configuration Options

- **`name`**: Logger name (default: `'FoxCoffe'`).
- **`log_file`**: File name for logging (default: `'logError.log'`).
- **`level`**: Logging level (default: `logging.INFO`).
- **`console_log`**: Enable/disable console logging (default: `True`).
- **`file_log`**: Enable/disable file logging (default: `True`).
- **`logger_filename`**: Name of the logger file to exclude from tracebacks (default: `'logger.py'`).
- **`include_logger_in_traceback`**: Include the logger file in tracebacks (default: `False`).

---

## Examples

### Rotating Log File Example

```python
logger = CustomLogger(
    name='RotatingLogger',
    log_file='rotating.log',
    level=logging.DEBUG,
    console_log=False,
    file_log=True
)

for i in range(1000):
    logger.log_info(f"Logging message #{i}")
```

### Custom Exception Logging

```python
@logger.log_exception
def division(a, b):
    return a / b

try:
    division(5, 0)
except ZeroDivisionError:
    pass
```

---

## Log Levels

| Level     | Numeric Value | Description                          |
|-----------|---------------|--------------------------------------|
| `DEBUG`   | 10            | Detailed debug information.         |
| `INFO`    | 20            | General informational messages.     |
| `WARNING` | 30            | Warning messages.                   |
| `ERROR`   | 40            | Errors that occur during execution. |
| `CRITICAL`| 50            | Critical issues requiring attention.|

---

## How It Works

The `CustomLogger` class uses Python's `logging` module and `RotatingFileHandler` to manage log files efficiently. Handlers are added to route logs to the console and/or file as needed. The built-in `log_exception` decorator captures exceptions in decorated functions, logging them with detailed tracebacks.

---

## Contribution

Contributions are welcome! If you have ideas for new features or find any issues, feel free to create a pull request or open an issue.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

Developed by **Senhor Fox**. For questions or suggestions, feel free to contact me through my [YouTube Channel](https://youtube.com/@FoxpopPlay).
