# `cli.py` Documentation

## Module Description

The `cli.py` module serves as the command-line interface (CLI) for MeowDoc, a documentation generator that leverages Large Language Models (LLMs) and MkDocs. It handles argument parsing, configuration loading, LLM provider initialization, interactive mode, and ultimately orchestrates the documentation generation process.

## Dependencies

This module relies on the following external libraries:

-   `os`: For interacting with the operating system, such as accessing environment variables and checking file existence.
-   `dotenv`: For loading environment variables from a `.env` file.
-   `logging`: For logging messages during the execution of the script.
-   `argparse`: For parsing command-line arguments.
-   `toml`: For reading and parsing TOML configuration files.
-   `google.generativeai`: For interacting with the Gemini API.
-   `meowdoc.core`: For the core documentation generation logic.
-   `meowdoc.mkdocs`: For MkDocs project setup and navigation updates.
-   `meowdoc.llm`: For handling different LLM providers.

## Functions

### `main()`

```python
def main():
    """Main function to run MeowDoc."""
```

The `main` function is the entry point of the MeowDoc CLI application. It performs the following steps:

1.  **Initialization**: Sets up logging, loads environment variables, and configures the Gemini API.
2.  **Argument Parsing**: Creates an `ArgumentParser` instance, adds arguments using `add_parser_args()`, and parses the command-line arguments.
3.  **Configuration Loading**: Loads the configuration from a TOML file using `load_config()`.
4.  **Configuration Override**: Overrides configuration values with command-line arguments using `override_config_with_args()`.
5.  **LLM Provider Initialization**: Gets an LLM provider instance using `get_llm_provider()`.
6.  **Interactive Mode**: Handles interactive mode if enabled using `handle_interactive_mode()`.
7.  **Configuration Validation**: Validates the main configuration using `validate_main_config()`.
8.  **Configuration Extraction**: Extracts configuration values, using helper function defaults, for input path, MkDocs directory, documentation directory name, MkDocs creation flag, ignore patterns, project name, description, and repository URL.
9.  **Configuration Logging**: Logs the current configuration using `log_configuration()`.
10. **MeowdocCore Initialization**: Creates an instance of `MeowdocCore` with the loaded configuration.
11. **MkDocs Setup**: Sets up the MkDocs project using `handle_mkdocs_setup()`.
12. **Documentation Generation**: Processes the input path using `generator.process_path()` to generate documentation files.
13. **Project Index Creation**: Generates the project index page using `generator.create_project_index()`.
14. **MkDocs Navigation Update**: Updates the MkDocs navigation based on the generated files using `mkdocs.update_mkdocs_nav()`.
15. **Completion**: Logs a "Finished." message.

### `load_config(config_path)`

```python
def load_config(config_path):
    """Loads and validates the TOML configuration."""
```

This function loads a TOML configuration file from the specified `config_path`. It handles `FileNotFoundError` and `toml.TomlDecodeError` exceptions, logging error messages and returning `None` if an error occurs. It performs basic validation to ensure that the config file contains required sections ('main', 'ignore', 'project', and 'llm').

**Parameters:**

-   `config_path` (str): The path to the TOML configuration file.

**Returns:**

-   `dict`: A dictionary containing the configuration data, or `None` if an error occurred.

**Example Usage:**

```python
config = load_config("config.toml")
if config:
    print(config["main"]["input_path"])
```

### `override_config_with_args(config, args)`

```python
def override_config_with_args(config, args):
    """Overrides config values with command-line arguments."""
```

This function overrides configuration values with command-line arguments.  It prioritizes CLI arguments over the configuration file. It updates the `llm` section for provider, API key, base URL, and model. It extracts other relevant command line arguments to override values inside the `main` section.

**Parameters:**

-   `config` (dict): The configuration dictionary loaded from the TOML file.
-   `args` (argparse.Namespace): The parsed command-line arguments.

**Returns:**

-   `dict`: The updated configuration dictionary with overridden values.

**Example Usage:**

```python
config = override_config_with_args(config, args)
print(config["llm"]["provider"])  # Might be overridden by --provider argument
```

### `get_llm_provider(config)`

```python
def get_llm_provider(config):
    """Gets the LLM provider instance."""
```

This function retrieves an LLM provider instance based on the configuration. It calls `llm.get_llm_provider()` and handles `ValueError` exceptions, logging an error message and returning `None` if an error occurs.

**Parameters:**

-   `config` (dict): The configuration dictionary containing LLM provider settings.

**Returns:**

-   `llm.LLMProvider`: An instance of the LLM provider, or `None` if an error occurred.

**Example Usage:**

```python
llm_provider = get_llm_provider(config)
if llm_provider:
    response = llm_provider.generate("Generate a summary.")
```

### `handle_interactive_mode(config, args)`

```python
def handle_interactive_mode(config, args):
    """Handles interactive mode input."""
```

This function handles interactive mode, prompting the user for configuration values if the `--interactive` flag is set. It populates the configuration dictionary based on user input.

**Parameters:**

-   `config` (dict): The configuration dictionary.
-   `args` (argparse.Namespace): The parsed command-line arguments.

**Returns:**

-   `dict`: The updated configuration dictionary with user-provided values.

**Example Usage:**

```python
config = handle_interactive_mode(config, args)
print(config["main"]["input_path"])  # User-provided input path
```

### `validate_main_config(config, parser)`

```python
def validate_main_config(config, parser):
    """Validates the main configuration."""
```

This function validates the main configuration, ensuring that the `input_path` is set. If it is not set, it prints the help message and exits. If the "ignore" section or "patterns" key are missing, it adds a default set of ignore patterns.

**Parameters:**

-   `config` (dict): The configuration dictionary.
-   `parser` (argparse.ArgumentParser): The argument parser.

**Example Usage:**

```python
validate_main_config(config, parser)
```

### `handle_mkdocs_setup(mkdocs_dir, docs_dir_name, create_mkdocs)`

```python
def handle_mkdocs_setup(mkdocs_dir, docs_dir_name, create_mkdocs):
    """Handles MkDocs project creation."""
```

This function handles the MkDocs project setup. If `create_mkdocs` is `True`, it creates a new MkDocs project using `mkdocs.create_mkdocs_project()`. If the MkDocs project or the documentation directory doesn't exist, it creates a new MkDocs project.

**Parameters:**

-   `mkdocs_dir` (str): The directory for the MkDocs project.
-   `docs_dir_name` (str): The name of the documentation directory within the MkDocs project.
-   `create_mkdocs` (bool): A flag indicating whether to create a new MkDocs project.

**Example Usage:**

```python
handle_mkdocs_setup(mkdocs_dir, docs_dir_name, create_mkdocs)
```

### `log_configuration(config)`

```python
def log_configuration(config):
    """Logs the current configuration."""
```

This function logs the current configuration values, including the input path, model, MkDocs directory, documentation directory name, and ignore patterns.

**Parameters:**

-   `config` (dict): The configuration dictionary.

**Example Usage:**

```python
log_configuration(config)
```

### `add_parser_args(parser)`

```python
def add_parser_args(parser):
    """Adds command-line arguments to the parser."""
```

This function adds command-line arguments to the `ArgumentParser` instance. These arguments allow users to configure MeowDoc from the command line.

**Parameters:**

-   `parser` (argparse.ArgumentParser): The argument parser.

**Example Usage:**

```python
parser = argparse.ArgumentParser(description="Generate documentation using LLMs and MkDocs.")
add_parser_args(parser)
args = parser.parse_args()
```

## Usage Examples

### Running MeowDoc with a configuration file

```bash
python cli.py -c config.toml
```

### Running MeowDoc in interactive mode

```bash
python cli.py --interactive
```

### Overriding configuration values with command-line arguments

```bash
python cli.py -c config.toml --provider openai --api-key YOUR_API_KEY --input_path ./my_project
```

### Creating MkDocs project along with documentation

```bash
python cli.py --create-mkdocs -c config.toml
```

## Related Files

-   `core.py`: Contains the core logic for generating documentation from Python files using LLMs.
-   `mkdocs.py`: Contains functions for creating and updating MkDocs projects and navigation.
-   `llm.py` (Not provided in the original documentation, but assumed to exist):  Handles the interaction with different LLM providers (Gemini, OpenAI, Ollama, etc.).
-   `themes.py`: Contains themes configurations and enable_theme function.
-   `config.toml` (Example): An example TOML configuration file:

    ```toml
    [main]
    input_path = "path/to/your/project"
    mkdocs_dir = "docs"
    docs_dir_name = "docs"
    create_mkdocs = false

    [ignore]
    patterns = [".venv", "venv", "node_modules", ".git", "__pycache__", ".env", "requirements.txt"]

    [project]
    name = "My Project"
    description = "A brief description of my project."
    repo_url = "https://github.com/myusername/myproject"

    [llm]
    provider = "gemini"
    model = "gemini-pro"
    api_key = "YOUR_GEMINI_API_KEY" # Or set GOOGLE_API_KEY env var
    ```

## Notes

-   The `GOOGLE_API_KEY` environment variable must be set for the Gemini API to function correctly, unless overridden by the `--api-key` command-line argument or interactive mode.
-   The configuration file `config.toml` is used to store default settings for the documentation generation process.
-   The `MeowdocCore` class in `core.py` handles the main logic for processing files and generating documentation.
-   The `mkdocs.py` module is responsible for creating and updating the MkDocs project based on the generated documentation.
- The LLM abstraction allows for swapping the LLM provider without rewriting the core logic. The interaction with the providers is handled by `meowdoc.llm`.
