# Steno™ - AI Chat Recorder


## 1. Installing Steno

### from git repo (Ubuntu 22.04.4 LTS, amd64)

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


## 2. Setting Up a Dedicated GitHub Repository and Token

### Step 1: Create a Dedicated Repository

- Log into your GitHub account.
- Click the **New** button on the repository page or navigate directly to [Create a new repository](https://github.com/new).
- Name the repository something specific, such as `username/username-steno-transcripts`, where `username` is your GitHub username. This clearly designates that the repository is used for storing Steno transcripts.
- Choose whether the repository should be public or private. A private repository is recommended for sensitive information.
- Initialize the repository with a README to help describe the purpose and setup of the repository.

### Step 2: Generate a Personal Access Token**:

- After logging in to GitHub, click on your profile photo in the upper-right corner and select **Settings**.
- In the sidebar, select **Developer settings**.
- Click on **Personal access tokens**, then **Generate new token**.
- Enter a descriptive name for the token, such as "Steno Access Token".

To ensure Steno operates correctly with your GitHub repository, it's essential to assign the correct permissions when creating your GitHub token. Below is a table of the required permissions and their access levels:

| Permission | Access Level | Description |
|------------|--------------|-------------|
| Contents   | Read & Write | Allows Steno to create, update, and delete transcript files in the repository. |
| Metadata   | Read-only    | Required for basic operations such as retrieving repository information necessary for commits and file management. |
| Commit statuses | Read-only | Useful if Steno needs to verify that transcripts were successfully added or to check the status of a commit. |
| Pull requests | Read & Write | Necessary only if Steno is designed to handle pull requests for adding transcripts, enabling it to manage PRs, comments, and merges related to transcript files. |

Ensure you select only the permissions that are necessary for the operations Steno needs to perform. This adherence to the principle of least privilege helps maintain the security of your repository.

### Step 3: Copy and Secure the Token

- After selecting the permissions, scroll down and click **Generate token**.
- Make sure to copy your new personal access token. GitHub will show you the token only once. If you lose it, you will have to regenerate a new one.
- Store this token securely within your configuration file, under a specific section that is properly secured and not accessible by unauthorized users.

**Using the Token Securely**

- **Secure the Configuration File**: Ensure that your Steno configuration file, which now contains your GitHub token, is secured. Restrict file permissions to prevent unauthorized access.

- **Regular Audits and Token Rotation**: Periodically check the security of your configuration file and rotate your GitHub token to enhance security. Make sure to update your configuration file with the new token promptly after rotation.


## 3. Configuring Steno

Certainly! Below is the revised section for your `README.md` that focuses on setting up and securing the configuration file for Steno, excluding advice on environment variables.

### Step 1: Create Configuration File

To configure Steno for your environment, you'll start by setting up the configuration file from a provided template. Here’s how to do it:

1. **Copy the Template**:
   From the root of the cloned Steno repository, locate `steno.example.yaml`. This file needs to be copied to your system's configuration directory.

   Use the following command to copy the file:

   ```bash
   cp steno.example.yaml ~/.config/steno/steno.yaml
   ```

   If the directory doesn’t exist, create it using:

   ```bash
   mkdir -p ~/.config/steno
   ```

2. **Modify the Configuration**:
   Edit `~/.config/steno/steno.yaml` with your preferred text editor to customize the settings to fit your needs:

   ```bash
   nano ~/.config/steno/steno.yaml
   ```

   Modify essential sections such as:
   - `ai`: Define the AI service and model to use.
   - `repository`: Input your GitHub repository path and authentication token.
   - `logging`: Set your preferred logging path, level, and rotation.

### Step 2: Secure the Configuration File

After configuring `steno.yaml`, ensure the file is secured since it may contain sensitive information like your GitHub token:

- **Restrict File Permissions**:
  Restrict the access permissions of your configuration file to prevent unauthorized access. Only the user account running Steno should have read access to this file. You can set these permissions using the following command:

  ```bash
  chmod 600 ~/.config/steno/steno.yaml
  ```

- **Regular Audits**:
  Periodically check the security settings of your configuration file to ensure they haven't been altered unintentionally.

Properly setting up and securing your `steno.yaml` is crucial for the smooth and secure operation of Steno. Ensure that you verify the functionality by running Steno in a test environment before going live. If you encounter issues or errors, refer to the troubleshooting section of this README or contact support through the GitHub repository issue tracker.


## 4. Using Steno

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
