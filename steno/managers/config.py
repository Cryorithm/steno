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
    def __init__(self):
        # Initialize with default settings except for 'api_key' since it should only
        # come from config file.
        self.config = {
            "ticker": "DASH",
            "destination": "log",
        }

    def load_yaml(self, path):
        resolved_path = Path(path).expanduser()
        try:
            with resolved_path.open("r") as f:
                config_data = yaml.safe_load(f)
                if config_data:
                    self.config.update(
                        config_data,
                    )  # Update all config values including api_key from file.
        except FileNotFoundError:
            print(
                "YAML configuration file not found at",
                resolved_path,
                ". Using defaults.",
            )
        except yaml.YAMLError as exc:
            print("Error parsing YAML file:", exc)

    def load_env_vars(self):
        # Load environment variables but exclude 'api_key'
        env_keys = ["ticker", "destination"]
        for key in env_keys:
            env_value = os.getenv(f"STENO_{key.upper()}")
            if env_value:
                self.config[key] = env_value

    def update_from_cli(self, cli_args):
        # Update configuration from CLI arguments excluding 'api_key'
        allowed_cli_keys = [
            "ticker",
            "destination",
        ]
        filtered_cli_args = {
            k: v for k, v in cli_args.items() if k in allowed_cli_keys and v is not None
        }

        self.config.update(filtered_cli_args)

    def get_config(self):
        return self.config
