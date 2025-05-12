# `meowdoc` Package

## Overview

The `meowdoc` package provides a tool for automatically generating documentation for Python projects using Large Language Models (LLMs) and integrating it with MkDocs. It streamlines the process of creating and maintaining project documentation by leveraging the power of AI to analyze code and generate comprehensive documentation in Markdown format.

This document describes the top-level `__init__.py` file for the `meowdoc` package.

## `__init__.py`

```python
```

### Description

The `__init__.py` file in the `meowdoc` package serves as the package's entry point.  In this case, it's empty. This implies that all functionality of the `meowdoc` package is accessed through its submodules: `cli`, `core`, `llm`, `mkdocs`, and `themes`.

### Usage

To use `meowdoc`, you would typically interact with the `cli` module, which provides the command-line interface for running the documentation generation process. The core functionality of generating documentation using LLMs is implemented in the `core` module. The `llm` module handles interactions with different LLM providers such as Gemini, OpenAI, and Ollama.  The `mkdocs` module handles the setup and updating of the MkDocs project to include generated documentation.

**Example:**

To run `meowdoc` from the command line, you would execute the `cli.py` file.  For example:

```bash
python cli.py -c config.toml
```

This command would run `meowdoc` using the configuration specified in the `config.toml` file.

## Related Modules

The `meowdoc` package consists of several modules that work together to generate documentation:

*   **`cli.py`**:  Provides the command-line interface for running `meowdoc`. It handles argument parsing, configuration loading, and orchestration of the documentation generation process.
*   **`core.py`**: Contains the core logic for processing files, generating documentation using LLMs, and creating the project index. The `MeowdocCore` class is the main class in this module.
*   **`llm.py`**: Defines the `LLMProvider` interface and concrete implementations for different LLM providers (Gemini, OpenAI, Ollama). It also includes the `get_llm_provider` function for initializing the appropriate LLM provider based on the configuration.
*   **`mkdocs.py`**:  Provides functions for creating and updating MkDocs projects.  It handles creating a new MkDocs project, updating the `mkdocs.yml` configuration file with generated documentation, and enabling the specified theme.
*   **`themes.py`**:  Defines available MkDocs themes and provides a function to install the selected theme using `pip`.

## Overall Functionality

The `meowdoc` package automates the process of generating documentation for Python projects by:

1.  **Loading configuration:**  The `cli.py` module loads configuration from a TOML file and command-line arguments.
2.  **Processing files:** The `core.py` module recursively traverses the input path, identifies Python files, and reads their contents.
3.  **Generating documentation:** The `core.py` module uses an LLM (configured via the `llm.py` module) to generate Markdown documentation for each file, considering the context of other files in the project.
4.  **Integrating with MkDocs:** The `mkdocs.py` module updates the MkDocs project to include the generated documentation in the navigation and configuration.
5.  **Docguide integration**: The core.py module processes the `/docguide/(pages)` directory where AI-generated or direct markdown file can be used to add to the mkdocs documentation output.

By combining these modules, `meowdoc` provides a powerful and flexible solution for generating high-quality documentation for Python projects.
