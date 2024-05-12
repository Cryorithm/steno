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

import copy
import os
import yaml
from pathlib import Path

from jsonschema import validate, ValidationError


class ConfigManager:
    def __init__(self, log_manager):
        self.log_manager = log_manager
        self.config = {  # NOTE: Some settings should NOT have defaults.
            "ai": {
                "model": "openai:gpt-3.5",
            },
        }

    def get_yaml_schema(self):
        """
        Returns the base JSON schema used for initial YAML configuration validation.
        """
        return {
            "type": "object",
            "properties": {
                "ai": {
                    "type": "object",
                    "properties": {
                        "model": {"type": "string"},
                        "tokens": {
                            "type": "object",
                            "properties": {
                                "openai": {"type": "string", "minLength": 1},
                            },
                            "anyOf": [{"required": ["openai"]}],
                        },
                    },
                    "required": ["tokens"],
                },
                "repo": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "token": {"type": "string"},
                    },
                    "required": ["token"],
                },
                "log": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "pattern": "^.+\\.log$"},
                        "level": {
                            "type": "string",
                            "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        },
                        "rotation": {"type": "string"},
                    },
                    "required": [],
                },
            },
            "required": ["ai", "repo"],
        }

    def get_final_schema(self):
        """
        Returns the modified JSON schema for final configuration validation after
        merging all sources.
        """
        schema = self.get_yaml_schema()
        schema = copy.deepcopy(schema)
        schema["properties"]["ai"]["required"] = ["model", "tokens"]
        schema["properties"]["repo"]["required"] = ["id", "token"]
        schema["properties"]["log"]["required"] = ["path", "level", "rotation"]
        return schema

    def integrate_and_validate_all_configs(self, cli_args):
        """
        Integrates environment variables and command-line arguments into the existing
        configuration, and validates the final combined configuration. This method
        ensures that the configuration is complete and valid after all potential
        sources have been considered.

        This process involves three main steps:
        1. Loading and applying environment variables that might override existing
           configuration settings.
        2. Updating the configuration with any command-line arguments provided at
           runtime, which take precedence over all other sources.
        3. Validating the final configuration using a predefined JSON schema to ensure
           all required settings are correctly specified and that the configuration
           adheres to expected standards.

        Args:
            cli_args (dict): A dictionary containing command-line arguments. These
                             arguments are expected to align with the keys in the
                             configuration dictionary and provide the final layer of
                             configuration values.

        Raises:
            ValueError: If the final configuration does not validate against the JSON
                        schema, indicating that some required settings are missing or
                        malformed.

        This method is critical for ensuring the application is correctly configured
        before proceeding with operation, thereby preventing runtime errors due to
        configuration issues.
        """
        # Integrate environment variables
        self.load_env_vars()

        # Update from CLI arguments
        self.update_from_cli(cli_args)

        # Validate final configuration
        self.validate_config(self.config, self.get_final_schema(), "Final")

    def load_yaml_and_validate(self, path):
        """
        Load configuration settings from a YAML file and validate them to the schema.

        Args:
            path (str): The path to the YAML file to be loaded.
        """
        resolved_path = Path(path).expanduser()
        try:
            with resolved_path.open("r") as f:
                config_data = yaml.safe_load(f)
                if config_data:
                    self.config.update(config_data)
            self.validate_config(self.config, self.get_yaml_schema(), "YAML")
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
        ai_model = os.getenv("STENO_AI_MODEL")
        if ai_model:
            self.config["ai"]["model"] = ai_model

        repo_id = os.getenv("STENO_REPO_ID")
        if repo_id:
            self.config["repo"]["id"] = repo_id

    def update_from_cli(self, cli_args):
        """
        Update configuration settings from command-line arguments.

        Args:
            cli_args (dict): A dictionary of command-line arguments where keys match
                             the config keys.
        """
        filtered_cli_args = {
            "ai": {},
            "repo": {},
        }
        if "ai_model" in cli_args and cli_args["ai_model"] is not None:
            filtered_cli_args["ai"]["model"] = cli_args["ai_model"]
        if "repo_id" in cli_args and cli_args["repo_id"] is not None:
            filtered_cli_args["repo"]["id"] = cli_args["repo_id"]
        self.config.update(filtered_cli_args)

    def validate_config(self, config, schema, stage):
        """
        Validate the current configuration using JSON Schema.

        Args:
            config (dict): Configuration to validate.
            schema (dict): One of yaml or final JSON schema dictionaries.
            stage (str): Describes the stage at which validation is being performed.
        """
        try:
            validate(instance=config, schema=schema)
            self.log_manager.debug(f"{stage} configuration is valid.")
        except ValidationError as e:
            self.log_manager.error(
                f"{stage} configuration validation error: {e.message}",
            )
            raise ValueError(f"{stage} configuration validation failed: {e.message}")

    def get_config(self):
        """
        Get the current configuration dictionary.

        Returns:
            dict: The current configuration settings.
        """
        return self.config
