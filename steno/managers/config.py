"""
Steno™ | Managers | Config
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

import os
import yaml
from pathlib import Path


class ConfigManager:
    def __init__(self, log_manager):
        """
        Initialize the configuration manager with a LogManager instance.

        Args:
            log_manager (LogManager): The LogManager instance to handle logging.
        """
        self.log_manager = log_manager
        self.config = {  # NOTE: A default repo should not be defined.
            "ai": "openai:gpt-3.5",
        }

    def load_yaml(self, path):
        """
        Load configuration settings from a YAML file.

        Args:
            path (str): The path to the YAML file to be loaded.
        """
        resolved_path = Path(path).expanduser()
        try:
            with resolved_path.open("r") as f:
                config_data = yaml.safe_load(f)
                if config_data:
                    self.config.update(config_data)
        except FileNotFoundError:
            self.log_manager.info(
                f"YAML configuration file not found at {resolved_path}."
                "Using defaults.",
            )
        except yaml.YAMLError as exc:
            self.log_manager.error(f"Error parsing YAML file: {exc}")

    def load_env_vars(self):
        """
        Load configuration settings from environment variables prefixed with 'STENO_'.
        """
        env_keys = ["ai", "repo"]
        for key in env_keys:
            env_value = os.getenv(f"STENO_{key.upper()}")
            if env_value:
                self.config[key] = env_value

    def update_from_cli(self, cli_args):
        """
        Update configuration settings from command-line arguments.

        Args:
            cli_args (dict): A dictionary of command-line arguments where keys match
                             the config keys.
        """
        allowed_cli_keys = ["ai", "repo"]
        filtered_cli_args = {
            k: v for k, v in cli_args.items() if k in allowed_cli_keys and v is not None
        }
        self.config.update(filtered_cli_args)

    def validate_config(self):
        """
        Validate the current configuration to ensure all necessary keys are present.

        Raises an exception and terminates the program if a required configuration key
        is missing.
        """
        required_keys = ["ai", "repo"]
        for key in required_keys:
            if not self.config.get(key):
                self.log_manager.error(f"Missing configuration key: {key}")
                raise ValueError(
                    f"Configuration validation failed: Missing key '{key}'",
                )
        self.log_manager.info("Configuration is valid.")

    def get_config(self):
        """
        Get the current configuration dictionary.

        Returns:
            dict: The current configuration settings.
        """
        return self.config
