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
# TODO: Add ClaudeClient
# TODO: Add GeminiClient

import click
from steno.clients.openai import OpenAIClient

# from steno.clients.claude import ClaudeClient
# from steno.clients.gemini import GeminiClient
from steno.managers.config import ConfigManager
from steno.managers.log import LogManager
from steno.managers.transcript.github import GitHubTranscriptManager


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
@click.option(
    "--ai-model",
    type=click.Choice(["openai", "claude", "gemini"], case_sensitive=False),
    help="Select the AI model to interact with.",
)
@click.option(
    "--repo",
    help="GitHub (or similar) repository for storing transcripts (e.g. 'foo/chats').",
)
def main(config_path, log_path, log_level, log_rotation, ai_model, repo):
    # Initialize LogManager
    log_manager = LogManager(sink=log_path, level=log_level, rotation=log_rotation)
    log_manager.info("Application started", event="startup")
    log_manager.info(f"Log level set to {log_level}")

    # Initialize ConfigManager
    #
    # ConfigManager loads configurations in a prioritized order:
    # 1. Default Configuration: Predefined settings in the application.
    # 2. YAML Configuration: Settings loaded from a user-specified YAML file.
    # 3. Environment Variables: Settings overridden by environment variables.
    # 4. Command Line Arguments: Settings specified at runtime take highest precedence.
    config_manager = ConfigManager()
    config_manager.load_yaml(config_path)
    config_manager.load_env_vars()
    cli_args = {}  # Keep this just in case we need it later.
    config_manager.update_from_cli(cli_args)
    config = config_manager.get_config()  # Returns the final version of the config.
    log_manager.info("ConfigManager activated.", extra=config, event="startup")

    # Initialize TranscriptManager
    transcript_manager = GitHubTranscriptManager(repo=repo)

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


if __name__ == "__main__":
    main()
