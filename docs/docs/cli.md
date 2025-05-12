```markdown
# `cli.py` Documentation

This module provides a command-line interface (CLI) for MeowDoc, a documentation generator that uses Large Language Models (LLMs) to automatically generate documentation for Python projects.  It handles argument parsing, configuration loading, LLM provider initialization, and orchestration of the documentation generation process.

## Overview

The `cli.py` script serves as the entry point for the MeowDoc application.  It performs the following key tasks:

1.  **Parses command-line arguments:**  Uses `argparse` to handle user-specified options and arguments, such as the configuration file path, input path, LLM provider, API key, and other settings.
2.  **Loads and validates configuration:** Loads settings from a TOML configuration file and overrides them with command-line arguments where specified. Configuration specifies the input path, ignore patterns, project details, and LLM configuration.
3.  **Initializes the LLM provider:**  Creates an instance of the specified LLM provider (e.g., Gemini, OpenAI, Ollama) using the provided API key or base URL.
4.  **Sets up the MkDocs project:**  Creates a new MkDocs project if one doesn't exist.
5.  **Orchestrates documentation generation:**  Uses the `MeowdocCore` class from `core.py` to process the input path, generate documentation for each file, process docguide pages, and create a project index.
6.  **Updates MkDocs configuration:**  Updates the `mkdocs.yml` file with the generated documentation structure and other project settings.
7.  **Logging:** Logs the configuration values for transparency and debugging.

## Dependencies

*   `os`:  For interacting with the operating system (e.g., loading environment variables, checking file paths).
*   `dotenv`:  For loading environment variables from a `.env` file.
*   `logging`: For logging information, warnings, and errors.
*   `argparse`: For parsing command-line arguments.
*   `toml`:  For loading and parsing TOML configuration files.
*   `meowdoc.core`:  Provides the `MeowdocCore` class for documentation generation.
*   `meowdoc.mkdocs`: Provides functions for interacting with MkDocs (e.g., creating projects, updating the navigation).
*   `meowdoc.llm`: Provides the LLM provider classes (e.g., `GeminiProvider`, `OpenAiProvider`, `OllamaProvider`).
*   `google.generativeai`:  For interacting with the Google Gemini API (conditionally imported and used within `llm.py`).

## Functions

### `main()`

```python
def main():
    """Main function to run MeowDoc."""
```

The main function is the entry point of the `cli.py` script. It orchestrates the entire documentation generation process.

**Process:**

1.  **Initialize logging:** Sets up basic logging configuration.
2.  **Load environment variables:** Loads environment variables from a `.env` file using `load_dotenv()`.  This is used to retrieve the Google API key.
3.  **Configure Google Generative AI:** Configures the `google.generativeai` library with the API key from the environment variables.
4.  **Create argument parser:** Creates an `ArgumentParser` object to handle command-line arguments.
5.  **Add arguments:** Calls `add_parser_args()` to add the available arguments to the parser.
6.  **Parse arguments:** Parses the command-line arguments using `parser.parse_args()`.
7.  **Load configuration:** Loads the TOML configuration file using `load_config()`.
8.  **Override configuration:** Overrides configuration values with command-line arguments using `override_config_with_args()`.
9.  **Get LLM provider:**  Gets the LLM provider instance using `get_llm_provider()`.
10. **Handle interactive mode:** Handles interactive mode to prompt for user inputs using `handle_interactive_mode()`.
11. **Validate Main config:** Validates the main configuration is valid using `validate_main_config()`.
12. **Extract config values:** Extracts configuration values from the loaded configuration.
13.  **Log configuration:** Logs the current configuration using `log_configuration()`.
14.  **Create DocumentationGenerator instance:** Creates an instance of the `MeowdocCore` class from `core.py`.
15.  **Handle MkDocs setup:** Creates the MkDocs project if `create_mkdocs` is true and if it doesn't exist.
16.  **Process the input path:**  Calls `generator.process_path()` to generate documentation for all files in the input path.
17.  **Process docguide pages:** Calls `generator.process_docguide_pages()` to include docguide pages in the project.
18.  **Create project index:** Calls `generator.create_project_index()` to create an `index.md` file.
19.  **Update MkDocs configuration:** Calls `mkdocs.update_mkdocs_nav()` and `mkdocs.update_mkdocs_config_from_toml()` to update the `mkdocs.yml` file with the generated documentation structure.

**Example Usage:**

```bash
python cli.py -c config.toml my_project/
```

This command runs MeowDoc with the configuration file `config.toml` and the input path `my_project/`.

### `load_config(config_path)`

```python
def load_config(config_path):
    """Loads and validates the TOML configuration."""
```

Loads and validates a TOML configuration file.

**Args:**

*   `config_path` (str):  The path to the TOML configuration file.

**Returns:**

*   `dict`:  The loaded configuration as a dictionary if successful.
*   `None`: If the file is not found or if there is an error parsing the TOML.

**Raises:**

*   `FileNotFoundError`: If the specified configuration file does not exist.
*   `toml.TomlDecodeError`: If the TOML file contains syntax errors.

**Validation:**

The function performs basic validation to ensure that the configuration file contains the required sections: "main", "ignore", "project", and "llm".

**Example:**

```python
config = load_config("config.toml")
if config:
    print("Configuration loaded successfully:", config)
else:
    print("Failed to load configuration.")
```

### `override_config_with_args(config, args)`

```python
def override_config_with_args(config, args):
    """Overrides config values with command-line arguments."""
```

Overrides configuration values with command-line arguments.

**Args:**

*   `config` (dict):  The configuration dictionary.
*   `args` (`argparse.Namespace`):  The parsed command-line arguments.

**Returns:**

*   `dict`:  The updated configuration dictionary.

**Process:**

The function iterates through the command-line arguments and overrides the corresponding values in the configuration dictionary.
Specific handling for `ignore` arguments:  The `ignore` argument, if specified, overrides the `ignore.patterns` setting in the configuration.
Only updates the "main" section with overrides to prevent unexpected behavior.

**Example:**

```python
config = {"main": {"input_path": "src/"}, "llm": {"provider": "gemini", "model": "gemini-pro"}}
args = argparse.Namespace(input_path="another_src/", provider="openai", api_key="YOUR_API_KEY")
updated_config = override_config_with_args(config, args)
print(updated_config)
# Expected Output: {'main': {'input_path': 'another_src/'}, 'llm': {'provider': 'openai', 'model': 'gemini-pro'}}
```

### `get_llm_provider(config)`

```python
def get_llm_provider(config):
    """Gets the LLM provider instance."""
```

Gets an instance of the LLM provider based on the configuration.

**Args:**

*   `config` (dict): The configuration dictionary.

**Returns:**

*   `LLMProvider`:  An instance of the LLM provider.
*   `None`: If the LLM provider could not be initialized.

**Raises:**

*   `ValueError`: If the LLM provider is not supported or if the required configuration parameters are missing.

**Example:**

```python
config = {"llm": {"provider": "gemini", "api_key": "YOUR_API_KEY", "model": "gemini-pro"}}
llm_provider = get_llm_provider(config)
if llm_provider:
    print("LLM provider initialized:", llm_provider)
else:
    print("Failed to initialize LLM provider.")
```

### `handle_interactive_mode(config, args)`

```python
def handle_interactive_mode(config, args):
    """Handles interactive mode input."""
```

Handles interactive mode, prompting the user for configuration values.

**Args:**

*   `config` (dict):  The configuration dictionary.
*   `args` (`argparse.Namespace`):  The parsed command-line arguments.

**Returns:**

*   `dict`: The updated configuration dictionary with user-provided values.

**Process:**

If the `--interactive` flag is set, the function prompts the user for the following configuration values:

*   `input_path`: Path to the input file or directory.
*   `model`: The Gemini model to use.
*   `create_mkdocs`: Whether to create the MkDocs project.
*   `mkdocs_dir`: The MkDocs project directory.
*   `docs_dir_name`: The docs directory name.
*   `ignore`: A comma-separated list of ignore patterns.

### `validate_main_config(config, parser)`

```python
def validate_main_config(config, parser):
    """Validates the main configuration."""
```

Validates the main configuration to ensure it is valid.

**Args:**

*   `config` (dict): The configuration dictionary.
*   `parser` (`argparse.ArgumentParser`): The argument parser.

**Process:**

Checks that the `input_path` is provided. If not, it prints the help message and exits.
If `ignore` section is not defined or `patterns` are not in the ignore section, then the section will be created with default values.

### `handle_mkdocs_setup(mkdocs_dir, docs_dir_name, create_mkdocs)`

```python
def handle_mkdocs_setup(mkdocs_dir, docs_dir_name, create_mkdocs):
    """Handles MkDocs project creation."""
```

Handles the creation of the MkDocs project.

**Args:**

*   `mkdocs_dir` (str):  The directory for the MkDocs project.
*   `docs_dir_name` (str): The name of the docs directory.
*   `create_mkdocs` (bool): A flag to create project if it doesn't exist.

**Process:**

*   Checks the `create_mkdocs` flag. If `create_mkdocs` is set to `True`, the `mkdocs.create_mkdocs_project()` will be called to create the project.
*   If `create_mkdocs` is set to `False`, then it will check whether the project exists in the given `mkdocs_dir`. If the project doesn't exist, the `mkdocs.create_mkdocs_project()` will be called to create the project.

### `log_configuration(config)`

```python
def log_configuration(config):
    """Logs the current configuration."""
```

Logs the current configuration for debugging and informational purposes.

**Args:**

*   `config` (dict): The configuration dictionary.

**Process:**

Logs the values of:

*   `input_path`
*   `model`
*   `mkdocs_dir`
*   `docs_dir_name`
*   `ignore_patterns`
*   `project name`

### `add_parser_args(parser)`

```python
def add_parser_args(parser):
    """Adds command-line arguments to the argument parser."""
```

Adds command-line arguments to the argument parser.

**Args:**

*   `parser` (`argparse.ArgumentParser`):  The argument parser object.

**Arguments:**

*   `-c, --config`: Path to the configuration file (default: `config.toml`).
*   `input_path`: Path to the Python file or directory.
*   `--create-mkdocs`:  Create mkdocs project if it doesn't exist.
*   `--mkdocs-dir`: Directory for the mkdocs project.
*   `--docs-dir-name`: Name of the docs directory inside the mkdocs project.
*   `--interactive`: Run in interactive mode.
*   `--ignore`: Ignore patterns (e.g., `.venv venv node_modules`).
*   `--provider`: LLM provider (gemini, openai, ollama).
*   `--api-key`: API key for the LLM provider.
*   `--base-url`: Base URL for local LLMs like Ollama.
*   `--model`: Model name for the LLM provider.

## Configuration

MeowDoc uses a TOML configuration file to store settings.  The configuration file should contain the following sections:

*   **`main`**: Contains the main settings for the documentation generation process.
    *   `input_path` (str):  The path to the Python file or directory to document.
    *   `mkdocs_dir` (str, optional): The directory for the MkDocs project (default: "docs").
    *   `docs_dir_name` (str, optional): The name of the docs directory inside the MkDocs project (default: "docs").
    *   `create_mkdocs` (bool, optional): Whether to create a new MkDocs project if one doesn't exist (default: `False`).

*   **`ignore`**:  Contains settings for ignoring files and directories.
    *   `patterns` (list of str):  A list of glob patterns to ignore (e.g., `[".venv", "venv", "node_modules"]`).

*   **`project`**:  Contains project-related information.
    *   `name` (str, optional): The name of the project.
    *   `description` (str, optional): A brief description of the project.
    *   `repo_url` (str, optional):  The URL of the project's repository.

*   **`llm`**: Contains settings for the LLM provider.
    *   `provider` (str):  The LLM provider to use (e.g., "gemini", "openai", "ollama").
    *   `api_key` (str, optional):  The API key for the LLM provider (required for Gemini and OpenAI).
    *   `base_url` (str, optional): The base URL for local LLMs like Ollama (required for Ollama).
    *   `model` (str): The name of the model to use.

**Example `config.toml`:**

```toml
[main]
input_path = "my_project/"
mkdocs_dir = "documentation"
docs_dir_name = "site"
create_mkdocs = false

[ignore]
patterns = [".venv", "venv", "node_modules"]

[project]
name = "My Project"
description = "A brief description of my project."
repo_url = "https://github.com/user/my_project"

[llm]
provider = "gemini"
api_key_file = ".secrets/gemini_api_key"
model = "gemini-pro"

[mkdocs]
site_name = "My Custom Name"
```

## Integration with Other Modules

*   **`core.py`:**  The `cli.py` module uses the `MeowdocCore` class from `core.py` to handle the core logic of documentation generation.  It passes the configuration values and LLM provider instance to the `MeowdocCore` constructor.
*   **`llm.py`:** The `cli.py` module uses functions from `llm.py` to initialize the LLM provider (e.g., `GeminiProvider`, `OpenAiProvider`, `OllamaProvider`). It passes the LLM-related configuration values to the `get_llm_provider()` function.
*   **`mkdocs.py`:** The `cli.py` module uses functions from `mkdocs.py` to interact with MkDocs, such as creating a new project (`create_mkdocs_project()`) and updating the `mkdocs.yml` file (`update_mkdocs_nav()`, `update_mkdocs_config_from_toml()`).
*   **`themes.py`**: The `cli.py` module uses functions from `themes.py` to install a theme.

## Error Handling

The `cli.py` module includes error handling to gracefully handle common issues, such as:

*   Configuration file not found or invalid.
*   Invalid LLM provider or missing API key.
*   Errors during documentation generation.
*   Errors during MkDocs project creation or configuration.

When an error occurs, the module logs an error message and exits with a non-zero exit code.
```