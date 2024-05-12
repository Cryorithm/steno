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

# TODO: Apply the interface/implementation pattern used for TranscriptManager to
#       ModelManager (or whatever we'll call it).
# TODO: Add some kind of object oriented fix to the AI functions.
# TODO: Add a LOT more test coverage.
# TODO: Add support for Claude
# TODO: Add support for Gemini

import click
from loguru import logger

# from steno.clients.openai import OpenAIClient

# from steno.clients.claude import ClaudeClient
# from steno.clients.gemini import GeminiClient
from steno.managers.config import ConfigManager
from steno.managers.log import LogManager

# from steno.managers.transcript.github import GitHubTranscriptManager


@logger.catch
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
    default="INFO",
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
@click.option(
    "--ai-model",
    help=(
        "Specify the AI model in the format 'service:model'. "
        "Examples: 'openai:gpt-4', 'openai:gpt-3.5-turbo-16k', "
        "'openai:gpt-4-turbo'."
    ),
)
@click.option(
    "--repo-id",
    help=(
        "GitHub or similar repository for storing transcripts "
        "(e.g., 'username/repository')."
    ),
)
def main(config_path, log_path, log_level, log_rotation, ai_model, repo_id):
    # Initialize LogManager
    log_manager = LogManager(sink=log_path, level=log_level, rotation=log_rotation)
    log_manager.debug("Application started.", event="startup")
    log_manager.debug(f"Log level set to {log_level}")

    # Initialize ConfigManager
    #
    # ConfigManager loads configurations in a prioritized order:
    # 1. Default Configuration: Predefined settings in the application.
    # 2. YAML Configuration: Settings loaded from a user-specified YAML file.
    # 3. Environment Variables: Settings overridden by environment variables.
    # 4. Command Line Arguments: Settings specified at runtime take highest precedence.
    #
    # NOTE: All secrets MUST be in the config file as they will not be loaded from
    #       elsewhere due to security concerns.
    config_manager = ConfigManager(log_manager)
    config_manager.load_yaml(config_path)
    config_manager.load_env_vars()
    cli_args = {
        "ai": {
            "model": ai_model,
        },
        "repo": {
            "id": repo_id,
        },
    }
    config_manager.integrate_and_validate_all_configs(cli_args)
    config = config_manager.get_config()  # Returns the final version of the config.
    log_manager.debug("ConfigManager activated.", extra=config, event="startup")

    # Initialize TranscriptManager
    # transcript_manager = GitHubTranscriptManager(
    #    log_manager=log_manager,
    #    repo=config["repo"]["id"],
    #    token=config["repo"]["token"],
    # )

    # Handle the user's AI selection.
    try:
        service, model = config["ai"]["model"].split(":")
        assert service and model  # Ensure both parts are not empty
        setup_model(service, model, log_manager)
    except (ValueError, AssertionError):
        log_manager.error(
            "Error: The --ai-model option must be in the format 'service:model'.",
        )


def setup_model(service, model, log_manager):
    if service == "openai":
        setup_openai_model(model, log_manager)
    else:
        log_manager.error(f"Unsupported AI service: {service}")


def setup_openai_model(model, log_manager):
    if model == "gpt-4":
        log_manager.info("Setting up OpenAI GPT-4...")
    elif model == "gpt-3.5":
        log_manager.info("Setting up OpenAI GPT-3.5...")
    elif model == "gpt-4-turbo":
        log_manager.info("Setting up OpenAI GPT-4 Turbo...")
    elif model == "gpt-3.5-turbo":
        log_manager.info("Setting up OpenAI GPT-3.5 Turbo...")
    else:
        log_manager.error(f"Unsupported model for OpenAI: {model}")


if __name__ == "__main__":
    main()

"""
    # AI Model Initialization
    ai_client = None
    if ai_model == "openai":
        ai_client = OpenAIClient()
    # elif ai_model == "claude":
    #    ai_client = ClaudeClient()
    # elif ai_model == "gemini":
    #    ai_client = GeminiClient()

    if ai_client:
        prompt = click.prompt("Enter your prompt for the AI", type=str)
        response = ai_client.get_response(prompt)
        log_manager.info(f"Received response: {response}")
        transcript_manager.log_conversation(prompt, response)
"""
