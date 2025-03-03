"""
Logging configuration for the py-pricer package.

This module sets up logging for the package with options for
console and file logging, as well as JSON formatting.
"""

import os
import logging
import logging.config
from pathlib import Path
from pythonjsonlogger import jsonlogger
from py_pricer import get_project_root
from py_pricer.config import LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT

def setup_logging(
    console_level=LOG_LEVEL,
    file_level=LOG_LEVEL,
    log_to_file=True,
    log_to_console=True,
    json_format=False,
    log_dir=None
):
    """
    Set up logging configuration for the application.
    
    Args:
        console_level: Logging level for console output
        file_level: Logging level for file output
        log_to_file: Whether to log to a file
        log_to_console: Whether to log to the console
        json_format: Whether to use JSON formatting for logs
        log_dir: Directory to store log files (defaults to logs/ in project root)
    """
    if log_dir is None:
        log_dir = os.path.join(get_project_root(), 'logs')
    
    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'py_pricer.log')
    
    handlers = {}
    
    if log_to_console:
        handlers['console'] = {
            'class': 'logging.StreamHandler',
            'level': console_level,
            'formatter': 'json' if json_format else 'standard',
            'stream': 'ext://sys.stdout',
        }
    
    if log_to_file:
        handlers['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': file_level,
            'formatter': 'json' if json_format else 'standard',
            'filename': log_file,
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        }
    
    formatters = {
        'standard': {
            'format': LOG_FORMAT,
            'datefmt': LOG_DATE_FORMAT,
        }
    }
    
    if json_format:
        formatters['json'] = {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
            'datefmt': LOG_DATE_FORMAT,
        }
    
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': formatters,
        'handlers': handlers,
        'loggers': {
            '': {  # Root logger
                'level': 'WARNING',
                'handlers': list(handlers.keys()),
            },
            'py_pricer': {
                'level': LOG_LEVEL,
                'handlers': list(handlers.keys()),
                'propagate': False,
            },
        }
    }
    
    logging.config.dictConfig(logging_config)
    logging.info(f"Logging configured. Log file: {log_file if log_to_file else 'None'}")

# Initialize logging with default settings
def init_logging():
    """Initialize logging with default settings."""
    # Check if logging should be configured from environment variables
    log_to_file = os.environ.get('PY_PRICER_LOG_TO_FILE', 'true').lower() == 'true'
    log_to_console = os.environ.get('PY_PRICER_LOG_TO_CONSOLE', 'true').lower() == 'true'
    json_format = os.environ.get('PY_PRICER_LOG_JSON', 'false').lower() == 'true'
    
    # Get log levels from environment variables or use defaults
    console_level_name = os.environ.get('PY_PRICER_CONSOLE_LOG_LEVEL', 'INFO')
    file_level_name = os.environ.get('PY_PRICER_FILE_LOG_LEVEL', 'DEBUG')
    
    console_level = getattr(logging, console_level_name.upper(), logging.INFO)
    file_level = getattr(logging, file_level_name.upper(), logging.DEBUG)
    
    # Set up logging
    setup_logging(
        console_level=console_level,
        file_level=file_level,
        log_to_file=log_to_file,
        log_to_console=log_to_console,
        json_format=json_format
    ) 