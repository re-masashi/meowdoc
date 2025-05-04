# `core.py`

## Module Description

This module defines the `MeowdocCore` class, which is the core component of the Meowdoc documentation generator. It leverages Large Language Models (LLMs) to automatically generate Markdown documentation for Python code, designed to be used with MkDocs. It handles file processing, interaction with LLMs, and the creation of MkDocs-compatible documentation files. The module facilitates the documentation process by reading Python code, prompting an LLM for documentation based on code context, and writing the generated documentation to Markdown files within a MkDocs project. The module also handles ignoring specified file patterns.

## `MeowdocCore` Class

### Overview

The `MeowdocCore` class orchestrates the documentation generation process.  It initializes with configuration parameters, processes input files or directories, interacts with a specified LLM, generates documentation for each file, and writes the resulting Markdown files. It is designed to work with multiple files by providing the LLM with context from other files in the same directory.

### Attributes

*   `input_path` (str): The path to the Python file or directory to document.
*   `mkdocs_dir` (str): The path to the root directory of the MkDocs project.
*   `docs_dir` (str): The name of the directory within the MkDocs project where the generated documentation will be placed.
*   `ignore_patterns` (list[str]): A list of filename patterns to ignore during the documentation process.  These patterns use `fnmatch` syntax.
*   `project_name` (str): The name of the project (used in the generated `index.md`).
*   `project_description` (str): A brief description of the project (used in the generated `index.md`).
*   `repo_url` (str): The URL of the project's repository (used in the generated `index.md`).
*   `llm_provider` (LLMProvider): An instance of a class derived from `LLMProvider` (defined in `llm.py`) which provides an interface to a Large Language Model.
#*   `model` (str, optional): The name of the LLM to use for generating documentation. Defaults to `"gemini-2.0-flash-exp"`.  (Commented out).

### Methods

#### `__init__(self, input_path, mkdocs_dir, docs_dir, ignore_patterns, project_name, project_description, repo_url, llm_provider)`

Initializes a new `MeowdocCore` instance.

*   **Parameters:**
    *   `input_path` (str): The path to the Python file or directory to document.
    *   `mkdocs_dir` (str): The path to the root directory of the MkDocs project.
    *   `docs_dir` (str): The name of the directory within the MkDocs project where the generated documentation will be placed.
    *   `ignore_patterns` (list[str]): A list of filename patterns to ignore during the documentation process.
    *   `project_name` (str): The name of the project.
    *   `project_description` (str): A brief description of the project.
    *   `repo_url` (str): The URL of the project's repository.
    *   `llm_provider` (LLMProvider): An instance of a class derived from `LLMProvider` (defined in `llm.py`) which provides an interface to a Large Language Model.
    #*   `model` (str, optional): The name of the LLM to use for generating documentation. Defaults to `"gemini-2.0-flash-exp"`. (Commented out)

*   **Returns:** None

*   **Example:**

    ```python
    from meowdoc import core
    from meowdoc import llm

    # Assuming you have an LLMProvider instance (e.g., GeminiProvider)
    # See llm.py for LLMProvider
    llm_provider = llm.GeminiProvider(api_key="YOUR_API_KEY", model="gemini-pro")

    generator = core.MeowdocCore(
        input_path="my_project",
        mkdocs_dir="mkdocs_site",
        docs_dir="reference",
        ignore_patterns=[".venv", "tests"],
        project_name="My Project",
        project_description="A simple example project.",
        repo_url="https://github.com/example/my_project",
        llm_provider=llm_provider,
    )
    ```

#### `generate_docs(self, file_path, all_file_contents)`

Generates documentation for a single file using an LLM, incorporating the content of related files for context.  It constructs a prompt that includes the target file's code and the code from all other files collected, and the documentation prompt. Optionally uses content from the `docguide` directory to provide additional guidance to the LLM.

*   **Parameters:**
    *   `file_path` (str): The path to the file to document.
    *   `all_file_contents` (dict[str, str]): A dictionary where keys are relative file paths (relative to input_path) and values are the file contents.

*   **Returns:** str | None
    *   The generated documentation in Markdown format, or `None` if an error occurred.

*   **Raises:**
    *   Logs an error message if the LLM call fails.

*   **Details:**
    1.  Constructs a prompt containing the target file's code and the code of related files as context for the LLM.
    2.  If a file exists in the `docguide` directory with a name matching the file path (e.g., `docguide/my_module.py.md`), it appends the contents of this file to the prompt as additional guidelines.
    3.  Calls the LLM to generate documentation based on the constructed prompt.
    4.  Returns the generated Markdown documentation.

*   **Example:**

    ```python
    # Example usage (assuming 'generator' is an instance of MeowdocCore)
    file_path = "my_module.py"
    all_file_contents = {
        "my_module.py": "def my_function():\n  \"\"\"A simple function\"\"\"\n  pass",
        "another_module.py": "def another_function():\n  pass"
    }
    documentation = generator.generate_docs(file_path, all_file_contents)
    if documentation:
        print(documentation)
    ```

#### `create_index(self, mkdocs_dir, docs_dir, readme_content)`

Creates the `index.md` file within the MkDocs `docs_dir` directory, populating it with the provided content.  This is not actively used since `create_project_index` performs a similar task, but generates an LLM-based description.

*   **Parameters:**
    *   `mkdocs_dir` (str): The path to the root directory of the MkDocs project.
    *   `docs_dir` (str): The name of the directory within the MkDocs project where the generated `index.md` will be placed.
    *   `readme_content` (str): The content to write to the `index.md` file.

*   **Returns:** None

*   **Example:**

    ```python
    # Example usage (assuming 'generator' is an instance of MeowdocCore)
    readme_content = "# My Project\n\nThis is the project's README."
    generator.create_index("mkdocs_site", "reference", readme_content)
    ```

#### `should_ignore(self, path, ignore_patterns)`

Checks if a given path (file or directory) or any of its parent directories should be ignored based on the provided `ignore_patterns`.

*   **Parameters:**
    *   `path` (str): The path to check.
    *   `ignore_patterns` (list[str]): A list of filename patterns to ignore (using `fnmatch` syntax).

*   **Returns:** bool
    *   `True` if the path or any of its parent directories match any of the `ignore_patterns`, `False` otherwise.

*   **Details:**
    *   Converts the path to an absolute path for consistent comparisons.
    *   Iterates through the path's parent directories, checking if each directory name matches any of the `ignore_patterns`.
    *   Uses `fnmatch.fnmatch` for pattern matching.

*   **Example:**

    ```python
    # Example usage (assuming 'generator' is an instance of MeowdocCore)
    ignore_patterns = [".venv", "tests"]
    print(generator.should_ignore(".venv/my_file.py", ignore_patterns))  # Output: True
    print(generator.should_ignore("src/my_file.py", ignore_patterns))  # Output: False
    print(generator.should_ignore("tests/my_file.py", ignore_patterns)) # Output: True
    ```

#### `_collect_files(self)`

Walks the `input_path` and returns a list of tuples `(file_path, relative_path)`, filtering out files matching the ignore patterns.

*   **Parameters:** None

*   **Returns:** list[tuple[str, str]]
    *   A list of tuples, where each tuple contains the absolute file path and the relative path (relative to the `input_path`).

*   **Details:**
    1.  Uses `os.walk` to traverse the directory tree starting at `self.input_path`.
    2.  For each file found, checks if the file or any of its parent directories should be ignored using `self.should_ignore`.
    3.  If a file should not be ignored, appends a tuple `(file_path, relative_path)` to the list.

*   **Example:**
    ```python
    # Assuming the following directory structure:
    # my_project/
    #   module1.py
    #   module2.py
    #   .venv/
    #     some_file.py

    # Assuming 'generator' is an instance of MeowdocCore with input_path="my_project"
    file_list = generator._collect_files()
    # Example output (order may vary):
    # [('my_project/module1.py', 'module1.py'), ('my_project/module2.py', 'module2.py')]

    ```

#### `process_path(self)`

Processes the input path (file or directory) to generate documentation.  This is the main method that drives the documentation generation process. This implementation uses concurrency via `ThreadPoolExecutor` to parallelize the documentation generation, significantly improving performance for larger projects.

*   **Parameters:** None

*   **Returns:** list[str]
    *   A list of paths to the generated documentation files.

*   **Details:**

    1.  Collects a list of files to process using `self._collect_files()`.
    2.  Pre-reads all file contents into memory for efficient access during parallel processing.
    3.  Creates the destination directory for the generated documentation files.
    4.  Uses a `ThreadPoolExecutor` to parallelize the documentation generation process:
        *   Submits each file to the `self.generate_docs` method for documentation generation.
        *   Writes the generated documentation to a Markdown file in the output directory, preserving the directory structure of the input files.
    5.  Returns a list of the generated documentation file paths.

*   **Example:**

    ```python
    # Example usage (assuming 'generator' is an instance of MeowdocCore)
    generated_files = generator.process_path()
    for file in generated_files:
        print(f"Generated documentation: {file}")
    ```

#### `create_project_index(self)`

Creates the `index.md` file for the MkDocs project, including a project description and a "Contributing" section generated by the LLM.

*   **Parameters:** None

*   **Returns:** None

*   **Details:**

    1.  Retrieves project name, project description and other attributes from the `MeowdocCore` instance.
    2.  Constructs prompts for the LLM to generate a project description and a "Contributing" section.
    3.  Calls the LLM to generate content for these sections.
    4.  Creates the `index.md` file in the MkDocs `docs_dir` directory.
    5.  Writes the generated project description and "Contributing" section, along with other standard content (e.g., installation instructions, license information), to the `index.md` file.

*   **Example:**

    ```python
    # Example usage (assuming 'generator' is an instance of MeowdocCore)
    generator.create_project_index()
    ```

## Interactions with Other Modules

*   **`llm.py`:** The `MeowdocCore` class interacts with the `llm.py` module to utilize LLMs for documentation generation. It receives an `LLMProvider` instance during initialization and calls its `generate` method to obtain documentation based on code context.
*   **`mkdocs.py`:** While `MeowdocCore` generates the documentation files, the `mkdocs.py` module is responsible for creating the MkDocs project (if it doesn't exist) and updating the `mkdocs.yml` configuration file to include the generated documentation in the site's navigation. The `cli.py` module handles calling functions in `mkdocs.py` based on the configuration provided to it.

## Usage Examples

See the examples in the method documentation above.  Also, see `cli.py` for how the `MeowdocCore` class is integrated into the command-line interface.

## Notes

*   Ensure that the LLM API key is properly configured in environment variables or through command-line arguments.
*   The quality of the generated documentation depends on the capabilities of the LLM and the clarity of the input code.
*   Consider creating `docguide` files to provide more specific instructions to the LLM.
