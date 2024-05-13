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
    """
    Manages the configuration of the application, loading settings in a prioritized
    order:

    1. Default Configuration: Predefined settings in the application.
    2. YAML Configuration: Settings loaded from a user-specified YAML file.
    3. Environment Variables: Settings overridden by environment variables.
    4. Command Line Arguments: Settings specified at runtime take the highest precedence.

    Secrets should not be loaded from external sources other than the config file for
    security reasons.

    Args:
        ctx (dict): A Click-style context dictionary.
        log_manager: A LogManager object.
    """

    def __init__(self, ctx, log_manager):
        """
        Initializes the ConfigManager with application context and a LogManager.

        Args:
            ctx (dict): A Click-style context dictionary.
            log_manager: A LogManager object.
        """
        self.__ctx = ctx
        self.__log_manager = log_manager

        # Load defaults.
        self.__load_defaults()

        # Load configuration from YAML.
        self.__load_yaml()

        # Validate configuration after loading from YAML.
        self.__validate_config(self.get_config(), self.__get_prep_schema(), "YAML")

        # Load configuration from environment variables.
        self.__load_env_vars()

        # Validate configuration after loading from environment variables.
        self.__validate_config(self.get_config(), self.__get_prep_schema(), "Env")

        # Debug.
        self.__debug()

        # Load configuration from CLI arguments.
        self.__load_cli_args()

        # Debug.
        self.__debug()

        # Validate final configuration.
        self.__validate_config(self.get_config(), self.__get_final_schema(), "Final")

        # Report activated.
        log_manager.debug(
            "ConfigManager activated.",
            extra=self.get_config(),
            event="startup",
        )

    def get_config(self):
        """
        Get the current configuration dictionary.

        Returns:
            dict: The current configuration settings.
        """
        return self.__config

    def __load_defaults(self):
        """
        Set a default config.

        NOTE: Some settings should not have default values.
        """
        self.__config = {
            "ai": {
                "model": "openai:gpt-3.5",
            },
        }

    def __debug(self):
        """Print things that help debug configuration issues."""
        things = {
            'ctx': self.__ctx,
            'config': self.get_config(),
        }
        print(
            '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',
            yaml.dump(things, allow_unicode=True, default_flow_style=False)),
            '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',
        )

    def __load_yaml(self, path):
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
                    self.__config.update(config_data)
        except FileNotFoundError:
            self.__log_manager.info(
                f"YAML configuration file not found at {resolved_path}."
                "Using defaults.",
            )
        except yaml.YAMLError as exc:
            self.__log_manager.error(f"Error parsing YAML file: {exc}")

    def __validate_config(self, schema, stage):
        """
        Validate the current configuration using JSON Schema.

        Args:
            config (dict): Configuration to validate.
            schema (dict): One of yaml or final JSON schema dictionaries.
            stage (str): Describes the stage at which validation is being performed.
        """
        try:
            validate(instance=self.__config, schema=schema)
            self.__log_manager.debug(f"{stage} configuration is valid.")
        except ValidationError as e:
            self.__log_manager.error(
                f"{stage} configuration validation error: {e.message}",
            )
            raise ValueError(f"{stage} configuration validation failed: {e.message}")

    def __get_prep_schema(self):
        """
        Returns the JSON Schema used to validate the early stages of activation.

        TODO: Consider setting schemas during init so that this manager can be used in
              other applications.
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

    def __get_final_schema(self):
        """
        Returns the modified JSON schema for final configuration validation after
        merging all sources.
        """
        schema = self.__get_prep_schema()
        schema = copy.deepcopy(schema)
        schema["properties"]["ai"]["required"] = ["model", "tokens"]
        schema["properties"]["repo"]["required"] = ["id", "token"]
        schema["properties"]["log"]["required"] = ["path", "level", "rotation"]
        return schema

    def __load_env_vars(self):
        """
        Load configuration settings from environment variables prefixed with 'STENO_'.
        """
        ai_model = os.getenv("STENO_AI_MODEL")
        if ai_model:
            self.__config["ai"]["model"] = ai_model

        repo_id = os.getenv("STENO_REPO_ID")
        if repo_id:
            self.__config["repo"]["id"] = repo_id

    def __load_cli_args(self):
        """
        Loads command line arguments from the Click context and carefully updates the
        configuration of ConfigManager.
        """
        # Fetch CLI arguments using context
        ai_model = self.__ctx.params.get('ai_model')
        repo_id = self.__ctx.params.get('repo_id')

        # Set these values in the configuration if they are provided
        if ai_model:
            self.__set_config_value(['ai', 'model'], ai_model)
        if repo_id:
            self.__set_config_value(['repo', 'id'], repo_id)

    def __set_config_value(self, path, value):
        """
        Private method to set a value in the ConfigManager's self.__config dictionary
        using a list of keys as the path.

        Creates nested dictionaries if necessary.

        Args:
            path (list): A list of keys representing the path to the target value.
            value: The value to set at the specified path.
        """
        config_dict = self.__config
        for key in path[:-1]:
            config_dict = config_dict.setdefault(key, {})
        if value is not None:
            config_dict[path[-1]] = value
