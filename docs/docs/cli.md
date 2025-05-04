# `cli.py` Documentation

## Overview

`cli.py` is the command-line interface for MeowDoc, a tool that generates documentation for Python projects using Large Language Models (LLMs) and MkDocs. It handles argument parsing, configuration loading and validation, LLM provider selection, and the overall workflow of documentation generation.

## Dependencies

*   `os`: For interacting with the operating system (e.g., accessing environment variables, checking file existence).
*   `dotenv`: For loading environment variables from a `.env` file.
*   `logging`: For logging messages and errors.
*   `argparse`: For parsing command-line arguments.
*   `toml`: For reading and parsing TOML configuration files.
*   `meowdoc.core`: Contains the core logic for processing files and generating documentation.
*   `meowdoc.mkdocs`: Contains functions for managing MkDocs projects and configurations.
*   `meowdoc.llm`: Contains classes for interacting with different LLM providers.
*   `google.generativeai`: For using Google's Gemini LLM (if selected).

## `main()` Function

The `main()` function is the entry point for the MeowDoc CLI. It orchestrates the entire documentation generation process.

### Function Signature

```python
def main():
```

### Functionality

1.  **Setup:**
    *   Configures basic logging to output errors.
    *   Loads environment variables from a `.env` file using `load_dotenv()`.  This is important for securing API keys.
    *   Configures the `google.generativeai` library if the Gemini LLM provider is used by initializing it with the API key from the environment variable `GOOGLE_API_KEY`.

2.  **Argument Parsing:**
    *   Creates an `ArgumentParser` instance to handle command-line arguments.
    *   Calls `add_parser_args()` to define the available arguments.
    *   Parses the arguments using `parser.parse_args()`.

3.  **Configuration Loading:**
    *   Loads the configuration from a TOML file specified by the `--config` argument (defaulting to `config.toml`).
    *   Calls `load_config()` to load and validate the configuration.  Exits if the configuration is invalid.

4.  **Configuration Overriding:**
    *   Overrides configuration values with command-line arguments using `override_config_with_args()`.  This allows users to customize the behavior of MeowDoc without modifying the config file.

5.  **LLM Provider Selection:**
    *   Retrieves the LLM provider instance using `get_llm_provider()`, based on the configuration.  Exits if the provider cannot be initialized.

6.  **Interactive Mode:**
    *   Handles interactive mode using `handle_interactive_mode()` if the `--interactive` flag is set. In interactive mode, the user is prompted for the input path, model, and other settings.

7.  **Main Configuration Validation:**
    *   Validates the main configuration using `validate_main_config()`, ensuring that at least the input path is provided.

8.  **Configuration Extraction:**
    *   Extracts configuration values into local variables:
        *   `input_path`: Path to the input file or directory.
        *   `mkdocs_dir`: Directory for the MkDocs project (default: "docs").
        *   `docs_dir_name`: Name of the "docs" directory within the MkDocs project (default: "docs").
        *   `create_mkdocs`: Boolean indicating whether to create a new MkDocs project if one doesn't exist (default: False).
        *   `ignore_patterns`: List of patterns to ignore when processing files.
        *   `project_name`: Name of the project.
        *   `description`: Description of the project.
        *   `repo_url`: URL of the project repository.

9.  **Configuration Logging:**
    *   Logs the loaded configuration using `log_configuration()`, providing a summary of the settings being used.

10. **Core Initialization:**
    *   Creates an instance of `core.MeowdocCore` with the extracted configuration values, passing in the LLM provider.

11. **MkDocs Setup:**
    *   Calls `handle_mkdocs_setup()` to create the MkDocs project if it doesn't exist, based on the `create_mkdocs` setting.

12. **Path Processing:**
    *   Calls `generator.process_path()` to process the input path and generate documentation for each file.

13. **Project Index Creation:**
    *   Calls `generator.create_project_index()` to generate the `index.md` file, which acts as the project's main page, leveraging the LLM for a description.

14. **MkDocs Update:**
    *   If any files were generated (`generated_files` is not empty):
        *   Calls `mkdocs.update_mkdocs_nav()` to update the `mkdocs.yml` file with the generated files.
        *   Calls `mkdocs.update_mkdocs_config_from_toml()` to merge the `mkdocs` section from `config.toml` into `mkdocs.yml`.
        *   Calls `mkdocs.finalize()` to deduplicate keys in the `mkdocs.yml` file, keeping the last occurrence.

15. **Finalization:**
    *   Prints a "All docs generated" message.
    *   Logs a "Finished" message using `logging.info()`.

## Helper Functions

### `load_config(config_path)`

Loads and validates the TOML configuration file.

#### Function Signature

```python
def load_config(config_path):
```

#### Parameters

*   `config_path`: The path to the TOML configuration file.

#### Functionality

1.  **File Reading:**
    *   Attempts to open and read the TOML file specified by `config_path`.
    *   Handles `FileNotFoundError` if the file does not exist, logging an error and returning `None`.
    *   Handles `toml.TomlDecodeError` if the file is not a valid TOML file, logging an error and returning `None`.

2.  **Basic Validation:**
    *   Checks for the existence of the `"main"`, `"ignore"`, `"project"`, and `"llm"` sections in the parsed configuration.
    *   Logs an error and returns `None` if any of these sections are missing.

3.  **Return Value:**
    *   Returns the parsed configuration as a dictionary if the file is successfully loaded and validated.  Otherwise, returns `None`.

### `override_config_with_args(config, args)`

Overrides configuration values with command-line arguments.

#### Function Signature

```python
def override_config_with_args(config, args):
```

#### Parameters

*   `config`: The configuration dictionary.
*   `args`: The parsed command-line arguments from `argparse`.

#### Functionality

1.  **Override LLM Configuration:**
    *   If the `--provider`, `--api-key`, `--base-url`, or `--model` arguments are provided, their values override the corresponding values in the `"llm"` section of the configuration.

2.  **Override Other Arguments:**
    *  Creates a dictionary `args_overrides` containing only the CLI arguments that have been passed in. The arguments "config", "interactive", and "create_mkdocs" are ignored.
    * If the `--ignore` argument is provided, it's popped from `args_overrides` and used to override the `"patterns"` list in the `"ignore"` section of the configuration.
    *   Updates the `"main"` section of the configuration with the remaining values from `args_overrides`.

3.  **Return Value:**
    *   Returns the modified configuration dictionary.

### `get_llm_provider(config)`

Gets the LLM provider instance based on the configuration.

#### Function Signature

```python
def get_llm_provider(config):
```

#### Parameters

*   `config`: The configuration dictionary containing LLM settings.

#### Functionality

1.  **Provider Retrieval:**
    *   Calls `llm.get_llm_provider()` to retrieve the appropriate LLM provider instance.

2.  **Error Handling:**
    *   Catches any `ValueError` raised by `llm.get_llm_provider()`, logs an error message, and returns `None`.

3.  **Return Value:**
    *   Returns the LLM provider instance if successful.  Otherwise, returns `None`.

### `handle_interactive_mode(config, args)`

Handles interactive mode input.

#### Function Signature

```python
def handle_interactive_mode(config, args):
```

#### Parameters

*   `config`: The configuration dictionary.
*   `args`: The parsed command-line arguments.

#### Functionality

1.  **Check for Interactive Mode:**
    *   Checks if the `--interactive` flag is set in the command-line arguments.  If not, the function does nothing.

2.  **Prompting for Configuration:**
    *   If interactive mode is enabled, the function prompts the user for various configuration values, including:
        *   `input_path`: The path to the input file or directory.
        *   `model`: The name of the Gemini model to use.
        *   `create_mkdocs`: Whether to create an MkDocs project.
        *   `mkdocs_dir`: The MkDocs project directory.
        *   `docs_dir_name`: The name of the docs directory.
        *   `ignore`: Ignore patterns separated by commas.

3. **Config Update:**
    *   The values entered by the user are then stored back into the `config` dictionary for use later.

4.  **Return Value:**
    * Returns the updated configuration dictionary.

### `validate_main_config(config, parser)`

Validates the main configuration.

#### Function Signature

```python
def validate_main_config(config, parser):
```

#### Parameters

*   `config`: The configuration dictionary.
*   `parser`: The `ArgumentParser` instance.

#### Functionality

1.  **Input Path Validation:**
    *   Checks if the `"input_path"` is present in the `"main"` section of the configuration.
    *   If not, prints the help message using `parser.print_help()` and exits with a code of 1.

2.  **Ignore Patterns Validation:**
    *   Checks if `"ignore"` or `"patterns"` exists in the config dictionary.
    *   If not, adds a default set of ignore patterns: `[".venv", "venv", "node_modules", ".git", "__pycache__", ".env", "requirements.txt"]`

### `handle_mkdocs_setup(mkdocs_dir, docs_dir_name, create_mkdocs)`

Handles MkDocs project creation.

#### Function Signature

```python
def handle_mkdocs_setup(mkdocs_dir, docs_dir_name, create_mkdocs):
```

#### Parameters

*   `mkdocs_dir`: The directory for the MkDocs project.
*   `docs_dir_name`: The name of the "docs" directory within the MkDocs project.
*   `create_mkdocs`: A boolean indicating whether to create a new MkDocs project if one doesn't exist.

#### Functionality

1.  **Create MkDocs Project (if needed):**
    *   If `create_mkdocs` is `True`, or if the `mkdocs_dir` and `docs_dir_name` do not exist, it attempts to create a new MkDocs project using `mkdocs.create_mkdocs_project()`.
    *   If project creation fails, it exits the program.

### `log_configuration(config)`

Logs the current configuration.

#### Function Signature

```python
def log_configuration(config):
```

#### Parameters

*   `config`: The configuration dictionary.

#### Functionality

1.  **Logging Configuration:**
    *   Logs the values of `input_path`, `model`, `mkdocs_dir`, `docs_dir_name`, and `ignore_patterns` using `logging.info()`.

### `add_parser_args(parser)`

Adds command-line arguments to the `ArgumentParser`.

#### Function Signature

```python
def add_parser_args(parser):
```

#### Parameters

*   `parser`: The `ArgumentParser` instance.

#### Functionality

Defines the following command-line arguments:

*   `-c`, `--config`: Path to the configuration file (default: `config.toml`).
*   `input_path`: Path to the Python file or directory.
*   `--create-mkdocs`: Create mkdocs project if it doesn't exist.
*   `--mkdocs-dir`: Directory for the mkdocs project.
*   `--docs-dir-name`: Name of the docs directory inside the mkdocs project.
*   `--interactive`: Run in interactive mode.
*   `--ignore`: Ignore patterns (e.g., `.venv venv node_modules`).
*   `--provider`: LLM provider (gemini, openai, ollama).
*   `--api-key`: API key for the LLM provider.
*   `--base-url`: Base URL for local LLMs like Ollama.
*   `--model`: Model name for the LLM provider.

## Usage

To use `cli.py`, run it from the command line with the desired arguments:

```bash
python cli.py <input_path> --config <config_file> --create-mkdocs --mkdocs-dir <mkdocs_directory> --docs-dir-name <docs_directory_name> --interactive --ignore <pattern1> <pattern2> ... --provider <provider> --api-key <api_key> --base-url <base_url> --model <model>
```

*   `<input_path>`: The path to the Python file or directory to document.
*   `<config_file>`: The path to the TOML configuration file. Defaults to `config.toml`.
*   `<mkdocs_directory>`: The directory where the MkDocs project should be created (if `--create-mkdocs` is used) or where it already exists.
*   `<docs_directory_name>`: The name of the directory within the MkDocs project where the generated documentation will be placed.
*   `<pattern1> <pattern2> ...`:  Space-separated list of ignore patterns.
*   `<provider>`:  The LLM provider to use (gemini, openai, or ollama).
*   `<api_key>`:  The API key for the LLM provider.
*   `<base_url>`: The base URL for local LLMs, like Ollama.
*   `<model>`: The model name for the LLM provider.

## Example Configuration (config.toml)

```toml
[main]
input_path = "my_project"  # Replace with your project's path
mkdocs_dir = "mkdocs"      # The mkdocs directory
docs_dir_name = "api_docs" # The docs directory name
create_mkdocs = false
# Add any other settings here that need to be passed into the core generator

[ignore]
patterns = [".venv", "venv", "node_modules", ".git", "__pycache__"] # Files and directories to ignore

[project]
name = "My Project"
description = "A brief description of my project."
repo_url = "https://github.com/user/my_project"

[llm]
provider = "gemini" # Can be "gemini", "openai", or "ollama"
api_key_file = "secrets/gemini_api_key.txt"  # Path to the API key file
# base_url = "http://localhost:11434"  # Only needed for ollama
model = "gemini-pro"  # The LLM model to use
# api_key = "YOUR_API_KEY" # Alternative way to define the API key.  Not recommended.

[mkdocs]
site_name = "My Project Documentation"
theme = {name = "material"}
```

## Related Files and Context

*   **`mkdocs.py`**:  Handles MkDocs project creation, configuration updates, and navigation generation.  The `cli.py` module calls functions from this file to manage the MkDocs project based on the generated documentation.  Specifically, the `update_mkdocs_nav` function is crucial for dynamically creating the navigation menu in `mkdocs.yml` based on the generated documentation files.

*   **`core.py`**: Contains the core logic for processing files, generating documentation prompts, and interacting with the LLM provider.  The `cli.py` module instantiates the `MeowdocCore` class from this file and calls its `process_path()` method to generate the documentation.

*   **`llm.py`**: Defines the `LLMProvider` base class and concrete implementations for different LLM providers (Gemini, OpenAI, Ollama).  The `cli.py` module uses the `get_llm_provider()` function from this file to create the appropriate LLM provider instance based on the configuration.

*   **`themes.py`**: Defines the themes for the MkDocs project.

*   **`__init__.py`**: An empty file that indicates that the directory should be treated as a Python package.

## Error Handling

The `cli.py` module includes comprehensive error handling:

*   **Configuration Loading:** Catches `FileNotFoundError` and `toml.TomlDecodeError` when loading the configuration file.
*   **LLM Provider Selection:** Catches `ValueError` when initializing the LLM provider.
*   **MkDocs Project Creation:** Handles exceptions during MkDocs project creation.
*   **File Reading:**  Handles exceptions during file reading within `MeowdocCore`.
*   **LLM Interaction:** Catches exceptions when calling the LLM API.
*   **MkDocs Configuration:** Catches exceptions when writing to `mkdocs.yml`

In case of errors, the script logs error messages using the `logging` module and exits with a non-zero exit code.
