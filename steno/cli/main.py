"""
Steno™ | CLI | Main
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


import click

# from steno.clients.openai import OpenAIClientWrapper
from steno.managers.config import ConfigManager
from steno.managers.log import LogManager


@click.command()
@click.option(
    "--config-path",
    type=click.Path(),
    default="~/.config/steno/config.yaml",
    show_default=True,
    envvar="STENO_CONFIG_PATH",
    help="Path to the configuration YAML file.",
)
@click.option(
    "--log-path",
    type=click.Path(),
    default="steno.log",
    show_default=True,
    envvar="STENO_LOG_PATH",
    help="Path to the log file.",
)
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        case_sensitive=False,
    ),
    default="DEBUG",
    show_default=True,
    envvar="STENO_LOG_LEVEL",
    help="Log level (case-insensitive).",
)
@click.option(
    "--log-rotation",
    default="10 MB",
    show_default=True,
    envvar="STENO_LOG_ROTATION",
    help="Log rotation configuration for the log file.",
)
@click.option("--ticker", help="Stock ticker symbol.")
@click.option(
    "--destination",
    type=click.Choice(["kafka", "log", "openai"]),
    help="Destination system where signals will be sent.",
)
@click.option(
    "--kafka-bootstrap-servers",
    help="Kafka bootstrap servers connection string.",
)
@click.option("--kafka-topic", help="Kafka topic where signals are sent.")
def main(
    config_path,
    log_path,
    log_level,
    log_rotation,
    ticker,
    destination,
    kafka_bootstrap_servers,
    kafka_topic,
):

    # Initialize LogManager
    log_manager = LogManager(sink=log_path, level=log_level, rotation=log_rotation)
    log_manager.info("Application started", event="startup")
    log_manager.info(f"Log level set to {log_level}")

    # Initialize ConfigManager
    config_manager = ConfigManager()

    # Load configurations in predefined order
    config_manager.load_yaml(config_path)
    config_manager.load_env_vars()

    # Prepare CLI arguments before passing them to update_from_cli
    cli_args = {
        "ticker": ticker,
        "destination": destination,
        "kafka_bootstrap_servers": kafka_bootstrap_servers,
        "kafka_topic": kafka_topic,
    }
    config_manager.update_from_cli(cli_args)
    config = config_manager.get_config()  # Returns the final version of the config.
    log_manager.info("ConfigManager activated.", extra=config, event="startup")


if __name__ == "__main__":
    main()
