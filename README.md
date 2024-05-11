# Steno™ - AI Chat Recorder

## Install from git repo (Windows 11, amd64)

_COMING SOON_

## Install from git repo (Ubuntu 22.04.4 LTS, amd64)

If you choose to install from the git repo, you will need to set up your development
environment to ensure everything functions correctly. Several `Makefile` commands can
facilitate this process.

Here's a step-by-step guide on what commands to run and in what order:

### Step 1: Install Python3, pip, pipx

Ensure Python is installed on your Ubuntu system. If not, you can install it along
with `pipx`:

```bash
sudo apt update
sudo apt install python3 python3-pip pipx
```

### Step 2: Install Poetry

Poetry is not typically included by default on Ubuntu, so you would need to install
it. You can do this by running the following command:

```bash
pipx install poetry
```

### Step 3: Activate the Poetry environment

```bash
make shell
```

### Step 4: Install project dependencies

```bash
make install
```

### Step 5: Install Project Dependencies and Set Up the Environment

This can typically be achieved by running `poetry install`, but since we use a
`Makefile`, the process can be initiated by:

```bash
make update
```

### Step 6: Install Pre-commit Hooks

After installing the pre-commit package, install the actual hooks configured for the
project:

```bash
make install-precommit
```

### Step 7: Run Initial Checks
To ensure everything is configured correctly (e.g., linters, formatters, and tests),
run:

```bash
make check
```

## Usage

_COMING SOON_


## License

```text
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
```
