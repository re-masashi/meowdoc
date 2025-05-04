```markdown
# `meowdoc` Package

This is the root package for `meowdoc`, a documentation generation tool that leverages LLMs and MkDocs.  It provides a convenient way to automatically generate documentation for Python projects.

## Overview

The `meowdoc` package contains several modules that work together to create a complete documentation workflow:

*   `core.py`: Contains the core logic for processing input files, generating documentation using LLMs, and creating an MkDocs project index.
*   `mkdocs.py`: Provides utilities for creating and updating MkDocs projects, including configuring the navigation and merging configuration files.
*   `themes.py`:  Defines available themes and provides functions for enabling them in MkDocs.
*   `cli.py`: Implements the command-line interface, allowing users to configure and run `meowdoc` from the terminal.
*   `llm.py`: Defines an abstract base class and concrete classes for interaction with various Language Models (LLMs)
*   `dummy_files/hw.rs`: A dummy file for testing.

## Package Structure

The package structure is as follows:

```
meowdoc/
├── __init__.py
├── core.py
├── mkdocs.py
├── themes.py
├── cli.py
├── llm.py
└── dummy_files/
    └── hw.rs
```

## Usage

To use `meowdoc`, you can install it using pip:

```bash
pip install meowdoc
```

Then, you can run it from the command line, providing the path to your project's source code:

```bash
meowdoc my_project
```

For more detailed usage instructions, refer to the documentation for `cli.py`.

## Module Details

### `core.py`

The `core.py` module contains the `MeowdocCore` class, which is responsible for:

*   Walking through the input path and identifying files to process.
*   Reading file contents.
*   Interacting with the LLM provider to generate documentation.
*   Creating the `index.md` file for the MkDocs project.

### `mkdocs.py`

The `mkdocs.py` module provides functions for:

*   Creating a new MkDocs project if one doesn't already exist.
*   Updating the `mkdocs.yml` configuration file with the generated documentation.
*   Merging configuration settings from a TOML file into the `mkdocs.yml` file.
*   Deduplicating keys from the `mkdocs.yml` file, keeping the last occurrence.

### `themes.py`

The `themes.py` module defines the available themes and provides a function to install and enable them:

*   `enable_theme(theme)`: Installs the specified theme using pip.

### `cli.py`

The `cli.py` module provides the command-line interface for `meowdoc`. It handles:

*   Parsing command-line arguments.
*   Loading the configuration file.
*   Initializing the LLM provider.
*   Running the documentation generation process.

### `llm.py`

The `llm.py` module defines an abstract base class and concrete classes for interaction with various Language Models (LLMs):
* `LLMProvider`: Abstract base class for LLM providers.
* `GeminiProvider`: LLM provider for Google Gemini.
* `OpenAiProvider`: LLM provider for OpenAI.
* `OllamaProvider`: LLM provider for Ollama (local LLM).
* `get_llm_provider`: Factory function for getting LLM provider instances

### `dummy_files/hw.rs`

A file for testing purposes.

## `__init__.py`

This file is intentionally left empty. It signifies that the current directory should be treated as a Python package.  It does not contain any code or perform any actions.
```