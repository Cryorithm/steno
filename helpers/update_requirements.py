"""
Update requirements.txt
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


import subprocess
from difflib import unified_diff


def get_requirements(command):
    """
    Common function to fetch and sort requirements,
    either from file or from poetry export
    """
    try:
        if command == "file":
            # Read from local requirements.txt if it exists
            with open("requirements.txt", encoding="utf-8") as file:
                requirements = [line.strip() for line in file if line.strip()]
        else:
            # Run poetry export and handle output
            result = subprocess.run(
                ["poetry", "export", "--without-hashes"],
                capture_output=True,
                text=True,
                check=True,
            )
            requirements = sorted(result.stdout.splitlines())
        return requirements
    except FileNotFoundError:
        return []
    except subprocess.CalledProcessError as e:
        print(f"Failed to export requirements: {e}")
        exit(1)


def update_requirements_file(new_requirements):
    # Updates the requirements.txt if necessary
    with open("requirements.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(new_requirements) + "\n")


def main():
    current_requirements = get_requirements("file")
    new_requirements = get_requirements("poetry")

    diff = list(
        unified_diff(
            current_requirements,
            new_requirements,
            fromfile="requirements.txt",
            tofile="new_requirements.txt",
        ),
    )

    if diff:
        print("Changes detected, updating requirements.txt.")
        print("\n".join(diff))
        update_requirements_file(new_requirements)
    else:
        print("No changes in requirements.txt detected.")


if __name__ == "__main__":
    main()
