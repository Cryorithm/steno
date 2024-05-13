"""
Steno™ | Managers | Log
"""

# Steno™ - AI Chat Recorder
#
# MIT License
#
# Copyright © 2024 Joshua M. Dotson (contact@cryorithm.org)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from loguru import logger


class LogManager:
    def __init__(self, sink=None, level="DEBUG", rotation="10 MB", serialize=True):
        """
        Initializes the LogManager with logging configuration.

        Args:
            sink (str, optional): An object, such as a pathlib.Path, in charge of
                receiving formatted logging messages and propagating them to an
                appropriate endpoint (see loguru.logger) (default: None)'
            level (str, optional): Logging level (default: 'DEBUG').
            rotation (str, optional): Log rotation configuration for the log file
                (default: '10 MB').
        """
        self.__sink = sink
        self.__rotation = rotation
        self.__serialize = serialize
        self.__level = level

        if self.__sink:
            logger.add(
                sink=self.__sink,
                level=self.__level,
                rotation=self.__rotation,
                serialize=self.__serialize,
                colorize=False,
            )
        logger.info("LogManager activated.", extra=self.get_config(), event="startup")

    def get_config(self):
        """
        Returns a dictionary containing the currently applied configuration.
        """
        return {
            "level": self.level,
            "sink": self.__sink,
            "rotation": self.__rotation,
            "serialize": self.__serialize,
        }

    def debug(self, message, *args, **kwargs):
        """Logs a debug message."""
        logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        """Logs an informational message."""
        logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """Logs a warning message."""
        logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """Logs an error message."""
        logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        """Logs a critical severity message."""
        logger.critical(message, *args, **kwargs)
