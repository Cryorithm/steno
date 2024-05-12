"""
Steno™ | Managers | Transcript | GitHub
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

import datetime
import sys

from github import Github, GithubException

from steno.managers.transcript.base import TranscriptManager


class GitHubTranscriptManager(TranscriptManager):
    """
    An implementation of TranscriptManager that logs conversations to a GitHub
    repository.
    """

    def __init__(self, log_manager, repo, token):
        """
        Initializes the GitHubTranscriptManager with the GitHub repository.

        :param repo: Path to the GitHub repository (e.g., 'username/repo').
        :param token: GitHub token for authentication (optional if token is set in
                      environment).
        :param log_manager: LogManager instance to handle logging.
        """
        self.repo = repo
        self.token = token
        self.github = Github(self.token)
        try:
            self.repo = self.github.get_repo(self.repo)
            log_manager.info(f"Successfully connected to GitHub repository: {repo}")
        except GithubException as e:
            log_manager.error(f"Failed to access GitHub repository: {repo}. Error: {e}")
            sys.exit(1)  # Exit the program if repository access fails

    def log_conversation(self, prompt, response):
        """
        Implements the logging of conversations to GitHub.

        :param prompt: The prompt sent to the AI.
        :param response: The response from the AI.
        """
        filename = f"Conversations/{datetime.datetime.now().isoformat()}.md"
        content = self._generate_conversation_content(prompt, response)

        try:
            self.repo.create_file(filename, "Log new conversation", content)
            self.log_manager.info("Conversation logged successfully.")
        except GithubException as e:
            self.log_manager.error(f"Failed to log conversation: {str(e)}")

    def _generate_conversation_content(self, prompt, response):
        """
        Generates formatted markdown content for logging the conversation.

        :param prompt: The prompt sent to the AI.
        :param response: The response from the AI.
        :return: Formatted markdown string.
        """
        content = f"## Prompt\n> {prompt}\n\n## Response\n> {response}\n\n---\n\n"
        return content
