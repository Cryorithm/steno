"""
Tests for steno/clients/openai.py
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

import pytest

from steno.clients.openai import OpenAIClientWrapper  # Assuming this is the path

def test_openai_client_init_with_key():
  """Test OpenAI client initialization with a provided API key"""
  api_key = "YOUR_API_KEY"  # Replace with your actual API key
  client = OpenAIClientWrapper(api_key=api_key)
  assert isinstance(client, OpenAIClientWrapper)  # Check if the object is of the expected class

# TODO: Fix/improve this test, or just drop it.
#def test_openai_client_init_no_key():
#    """Test OpenAI client initialization without a valid API key"""
#    dummy_key = "INVALID_KEY"  # Placeholder key (replace with actual logic for handling missing keys)
#    with pytest.raises(ValueError):  # Expect an error since the key is invalid
#        client = OpenAIClientWrapper(api_key=dummy_key)
