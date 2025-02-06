# `cli.py` Documentation

## Module Description

This module serves as the command-line interface (CLI) for MeowDoc. It handles argument parsing, configuration loading, LLM provider setup, interactive mode, MkDocs project creation, and orchestrates the documentation generation process using the `meowdoc` core library. The entry point is the `main` function, which is executed when the script is run.

## Table of Contents

- [Dependencies](#dependencies)
- [`main()` Function](#main-function)
- [Configuration Loading and Handling](#configuration-loading-and-handling)
  - [`load_config(config_path)` Function](#load_configconfig_path-function)
  - [`override_config_with_args(config, args)` Function](#override_config_with_argsconfig-args-function)
  - [`handle_interactive_mode(config, args)` Function](#handle_interactive_modeconfig-args-function)
  - [`validate_main_config(config, parser)` Function](#validate_main_configconfig-parser-function)
- [LLM Provider Setup](#llm-provider-setup)
  - [`get_llm_provider(config)` Function](#get_llm_providerconfig-function)
- [MkDocs Project Handling](#mkdocs-project-handling)
  - [`handle_mkdocs_setup(mkdocs_dir, docs_dir_name, create_mkdocs)` Function](#handle_mkdocs_setupmkdocs_dir-docs_dir_name-create_mkdocs-function)
- [Documentation Generation](#documentation-generation)
- [Logging](#logging)
  - [`log_configuration(config)` Function](#log_configurationconfig-function)
- [Argument Parsing](#argument-parsing)
  - [`add_parser_args(parser)` Function](#add_parser_argsparser-function)

## Dependencies

This module relies on the following external libraries:

-   `os`: For interacting with the operating system, such as accessing environment variables and checking file paths.
-   `dotenv`: For loading environment variables from a `.env` file.
-   `logging`: For logging messages and debugging information.
-   `argparse`: For parsing command-line arguments.
-   `toml`: For parsing TOML configuration files.
-   `meowdoc.core`:  For the core documentation generation logic (classes and functions).
-   `meowdoc.mkdocs`: For interacting with MkDocs (creating projects, updating navigation).
-   `meowdoc.llm`: For handling LLM provider selection and interaction.
-   `google.generativeai`: For interacting with the Gemini LLM (if selected).

## `main()` Function

The `main()` function orchestrates the entire documentation generation process:

1.  **Initialization:** Sets up logging, loads environment variables (including the Google API key), and configures the Gemini AI service.
2.  **Argument Parsing:** Creates an `ArgumentParser` object, adds arguments using `add_parser_args()`, and parses the command-line arguments.
3.  **Configuration Loading:** Loads the configuration from the specified TOML file using `load_config()`.  If no valid config is loaded, the program exits.
4.  **Configuration Override:** Overrides configuration values with command-line arguments using `override_config_with_args()`.
5.  **LLM Provider Setup:** Gets the appropriate LLM provider instance based on the configuration using `get_llm_provider()`. If no LLM provider is loaded, the program exits.
6.  **Interactive Mode:** Handles interactive mode, prompting the user for configuration values if enabled via the `--interactive` flag, using `handle_interactive_mode()`.
7.  **Configuration Validation:** Validates the main configuration using `validate_main_config()`.
8.  **Configuration Extraction:** Extracts configuration values such as the input path, MkDocs directory, ignore patterns, project name, and description.
9.  **Logging Configuration:** Logs the current configuration for debugging purposes, using `log_configuration()`.
10. **Core Initialization:** Initializes the `MeowdocCore` instance with the extracted configuration values and the LLM provider.
11. **MkDocs Setup:** Handles the creation of the MkDocs project if it doesn't exist, using `handle_mkdocs_setup()`.
12. **Documentation Generation:** Processes the input path (either a file or a directory) using `generator.process_path()`. This function generates the documentation files.
13. **Index Page Creation:** Creates the project's `index.md` file using `generator.create_project_index()`.
14. **MkDocs Navigation Update:** Updates the MkDocs navigation based on the generated files using `mkdocs.update_mkdocs_nav()`.
15. **Completion:** Logs a "Finished" message.

## Configuration Loading and Handling

This section describes the functions responsible for loading, validating, and overriding the configuration.

### `load_config(config_path)` Function

This function loads the TOML configuration file.

-   **Parameters:**
    -   `config_path` (str): The path to the TOML configuration file.
-   **Returns:**
    -   `dict`: A dictionary containing the configuration if the file is loaded and parsed successfully.
    -   `None`: If the file is not found or if there is an error parsing the TOML file.

The function performs basic validation to ensure that the configuration file contains the required sections ("main", "ignore", "project", and "llm"). If the file does not exist or parsing fails, it logs an error message and returns `None`.

**Example Usage:**

```python
config = load_config("config.toml")
if config:
    print(config["main"]["input_path"])
```

### `override_config_with_args(config, args)` Function

This function overrides configuration values with command-line arguments.

-   **Parameters:**
    -   `config` (dict): The configuration dictionary loaded from the TOML file.
    -   `args` (argparse.Namespace): The parsed command-line arguments.
-   **Returns:**
    -   `dict`: The updated configuration dictionary with overridden values.

The function iterates through the command-line arguments and updates the corresponding values in the configuration dictionary.  It prioritizes command-line arguments over the values specified in the configuration file. It specifically handles the `ignore` argument to allow overriding ignore patterns.

**Example Usage:**

```python
config = {"main": {"input_path": "src"}, "llm": {"provider": "openai"}}
args = argparse.Namespace(input_path="lib", provider="gemini", api_key=None, base_url=None, model=None, config="config.toml", interactive=False, create_mkdocs=False, mkdocs_dir=None, docs_dir_name=None, ignore=None)
updated_config = override_config_with_args(config, args)
print(updated_config["main"]["input_path"])  # Output: lib
print(updated_config["llm"]["provider"])  # Output: gemini
```

### `handle_interactive_mode(config, args)` Function

This function handles interactive mode, prompting the user for configuration values.

-   **Parameters:**
    -   `config` (dict): The configuration dictionary.
    -   `args` (argparse.Namespace): The parsed command-line arguments.
-   **Returns:**
    -   `dict`: The updated configuration dictionary with values provided by the user.

If the `--interactive` flag is set, this function prompts the user for the following configuration values:

-   Input path
-   Gemini model to use
-   Whether to create an MkDocs project if it doesn't exist
-   MkDocs project directory
-   Docs directory name
-   Ignore patterns (comma-separated)

The function updates the configuration dictionary with the user-provided values.

**Example Usage:**

```python
config = {"main": {}, "ignore": {}, "llm": {}}
args = argparse.Namespace(interactive=True, config="config.toml", input_path=None, create_mkdocs=False, mkdocs_dir=None, docs_dir_name=None, ignore=None, provider=None, api_key=None, base_url=None, model=None)
updated_config = handle_interactive_mode(config, args)
```

### `validate_main_config(config, parser)` Function

This function validates the main configuration.

-   **Parameters:**
    -   `config` (dict): The configuration dictionary.
    -   `parser` (argparse.ArgumentParser): The argument parser.
-   **Returns:**
    -   `None`

The function checks if the `input_path` is provided. If not, it prints the help message and exits. It also ensures that `ignore` and `patterns` exist within the config and sets default ignore patterns if needed.

## LLM Provider Setup

This section describes the function responsible for setting up the LLM provider.

### `get_llm_provider(config)` Function

This function gets the LLM provider instance.

-   **Parameters:**
    -   `config` (dict): The configuration dictionary containing LLM provider settings.
-   **Returns:**
    -   `meowdoc.llm.LLMProvider`: An instance of the selected LLM provider (e.g., GeminiLLM).
    -   `None`: If there is an error getting the LLM provider.

The function calls the `meowdoc.llm.get_llm_provider` function to get the LLM provider instance based on the configuration. If an error occurs (e.g., invalid provider name, missing API key), it logs an error message and returns `None`.  See `llm.py` for how this is handled.

**Example Usage:**

```python
llm_provider = get_llm_provider(config)
if llm_provider:
    print("LLM provider loaded successfully.")
```

## MkDocs Project Handling

This section describes the functions responsible for creating and managing the MkDocs project.

### `handle_mkdocs_setup(mkdocs_dir, docs_dir_name, create_mkdocs)` Function

This function handles MkDocs project creation.

-   **Parameters:**
    -   `mkdocs_dir` (str): The directory for the MkDocs project.
    -   `docs_dir_name` (str): The name of the "docs" directory inside the MkDocs project.
    -   `create_mkdocs` (bool): A flag indicating whether to create the MkDocs project if it doesn't exist.
-   **Returns:**
    -   `None`

If `create_mkdocs` is True or the `mkdocs_dir` and `docs_dir_name` don't both exist, the function calls `mkdocs.create_mkdocs_project()` to create the MkDocs project. If project creation fails, the program exits.

**Example Usage:**

```python
handle_mkdocs_setup("docs", "docs", True)
```

## Documentation Generation

The core of the documentation generation process is handled by the `MeowdocCore` class in the `core.py` module. The `cli.py` module instantiates this class and calls its `process_path()` method to generate the documentation files.  After the files are generated, `cli.py` calls `generator.create_project_index()` to make an index page describing the project. Finally it calls `mkdocs.update_mkdocs_nav()` to update the navigation in the `mkdocs.yml` file, linking to the generated documentation.

## Logging

The module uses the `logging` library to log messages and debugging information.

### `log_configuration(config)` Function

This function logs the current configuration.

-   **Parameters:**
    -   `config` (dict): The configuration dictionary.
-   **Returns:**
    -   `None`

The function logs the input path, model, MkDocs directory, docs directory name, and ignore patterns.

## Argument Parsing

The module uses the `argparse` library to parse command-line arguments.

### `add_parser_args(parser)` Function

This function adds arguments to the argument parser.

-   **Parameters:**
    -   `parser` (argparse.ArgumentParser): The argument parser.
-   **Returns:**
    -   `None`

The function adds the following arguments:

-   `-c`, `--config`: Path to the configuration file (default: config.toml).
-   `input_path`: Path to the Python file or directory.
-   `--create-mkdocs`: Create mkdocs project if it doesn't exist.
-   `--mkdocs-dir`: Directory for the mkdocs project.
-   `--docs-dir-name`: Name of the docs directory inside the mkdocs project.
-   `--interactive`: Run in interactive mode.
-   `--ignore`: Ignore patterns (e.g., .venv venv node_modules).
-   `--provider`: LLM provider (gemini, openai).
-   `--api-key`: API key for the LLM provider.
-   `--base-url`: Base URL for local LLMs like Ollama.
-   `--model`: Model name for the LLM provider.
