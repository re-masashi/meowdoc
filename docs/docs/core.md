```markdown
# `core.py` Documentation

This module defines the `MeowdocCore` class, which is the central component of Meowdoc. It's responsible for orchestrating the documentation generation process using LLMs (Language Model Models) and integrating with MkDocs to create the final documentation website. The core functionality includes file discovery, content extraction, prompt generation for the LLM, handling LLM responses, writing documentation to Markdown files, and creating project index files.  It also handles optional docguide pages.

## `MeowdocCore` Class

### Overview

The `MeowdocCore` class takes a directory of Python files as input and generates Markdown documentation for each file, leveraging a configured LLM to understand and document the code.  It supports ignoring files based on patterns, allows for customizing the project's name and description, and integrates with an LLM provider to generate documentation. It uses multithreading to speed up the documentation generation process.

### Initialization (`__init__`)

```python
def __init__(
    self, 
    input_path,
    mkdocs_dir,
    docs_dir,
    ignore_patterns,
    project_name,
    project_description,
    repo_url,
    llm_provider,
):
```

Initializes a `MeowdocCore` instance.

**Parameters:**

*   `input_path` (str): The path to the input directory containing Python files. This can also be a path to a single Python file.
*   `mkdocs_dir` (str): The directory where the MkDocs project resides.
*   `docs_dir` (str): The name of the directory within the MkDocs project where the generated documentation will be placed.
*   `ignore_patterns` (list[str]): A list of filename patterns to ignore during file discovery (e.g., `['*.pyc', 'test*']`).
*   `project_name` (str): The name of the project, used in the generated documentation and MkDocs configuration.
*   `project_description` (str): A brief description of the project, included in the generated documentation.
*   `repo_url` (str): The URL of the project's repository, included in the generated documentation.
*   `llm_provider` (LLMProvider): An instance of a configured LLM provider (e.g., `GeminiProvider`, `OpenAiProvider`, `OllamaProvider` from `llm.py`).

**Example:**

```python
from meowdoc import llm
# Assuming you have a config dictionary set up
llm_provider = llm.get_llm_provider(config)

core_instance = MeowdocCore(
    input_path="src",
    mkdocs_dir="mkdocs",
    docs_dir="api_docs",
    ignore_patterns=[".venv", "*.pyc"],
    project_name="MyProject",
    project_description="A sample project.",
    repo_url="https://github.com/example/myproject",
    llm_provider=llm_provider
)
```

### `generate_docs` Method

```python
def generate_docs(self, file_path, all_file_contents):
```

Generates documentation for a single Python file using the configured LLM.  It provides the LLM with the code to document *and* the content of all other related files in the project for context.  It also utilizes files in the `docguide` directory to inject additional guidelines into the prompt.

**Parameters:**

*   `file_path` (str): The absolute path to the Python file to document.
*   `all_file_contents` (dict[str, str]): A dictionary where the keys are the relative file paths (relative to `input_path`) and the values are the contents of each file.  This provides the LLM with context from related files.

**Returns:**

*   `str`: The generated Markdown documentation, or `None` if an error occurred.

**Functionality:**

1.  Constructs a prompt for the LLM that includes:
    *   The code of the target file.
    *   The code of all other files in `all_file_contents` for context.
    *   Instructions on the desired documentation format and content.
    *   Content of a `docguide` file (if it exists) to provide specific instructions for the file at `file_path`. The `docguide` file's path is derived from the `file_path`, e.g., if the file being documented is `src/my_module.py`, it looks for a docguide at `docguide/src/my_module.py.md`.

2.  Calls the `generate` method of the configured `llm_provider` to generate the documentation.
3.  Handles potential exceptions during the LLM call, logging errors.

**Example:**

```python
# Assuming core_instance is an instance of MeowdocCore
file_path = "src/my_module.py"
all_file_contents = {
    "src/my_module.py": "...",  # Content of my_module.py
    "src/another_module.py": "..."  # Content of another_module.py
}

documentation = core_instance.generate_docs(file_path, all_file_contents)

if documentation:
    print(documentation)
else:
    print("Documentation generation failed.")
```

### `should_ignore` Method

```python
def should_ignore(self, path, ignore_patterns):
```

Checks if a given file or directory path should be ignored based on a list of ignore patterns.  It checks not only the path itself, but also all parent directories.

**Parameters:**

*   `path` (str): The path to check.
*   `ignore_patterns` (list[str]): A list of filename patterns to ignore (e.g., `['*.pyc', 'test*']`).

**Returns:**

*   `bool`: `True` if the path or any of its parent directories should be ignored, `False` otherwise.

**Functionality:**

1.  Converts the input `path` to an absolute path.
2.  Iteratively checks if the base name of the path or any of its parent directories matches any of the `ignore_patterns` using `fnmatch.fnmatch`.
3.  Returns `True` if a match is found, indicating that the path should be ignored.

**Example:**

```python
# Assuming core_instance is an instance of MeowdocCore
path = "src/my_module.py"
ignore_patterns = [".venv", "*.pyc"]

if core_instance.should_ignore(path, ignore_patterns):
    print(f"Ignoring: {path}")
else:
    print(f"Not ignoring: {path}")
```

### `_collect_files` Method

```python
def _collect_files(self):
```

Walks the `input_path` directory and returns a list of all Python files that should be processed, excluding those matching the `ignore_patterns`.

**Returns:**

*   `list[tuple[str, str]]`: A list of tuples, where each tuple contains the absolute file path and the relative file path (relative to `input_path`) of a Python file to be processed.

**Functionality:**

1.  Uses `os.walk` to traverse the `input_path` directory tree.
2.  For each file found, it checks if the file or any of its parent directories should be ignored using the `should_ignore` method.
3.  If the file should not be ignored, it adds the absolute file path and the relative file path to the `file_list`.

**Example:**

```python
# Assuming core_instance is an instance of MeowdocCore
files = core_instance._collect_files()
for file_path, relative_path in files:
    print(f"File path: {file_path}, Relative path: {relative_path}")
```

### `process_path` Method

```python
def process_path(self):
```

Processes all the files collected in `_collect_files` and generates their documentation using `generate_docs`.  It uses a thread pool to parallelize the documentation generation process, improving performance.

**Returns:**

*   `list[str]`: A list of paths to the generated Markdown files.

**Functionality:**

1.  Collects the list of files to process using `_collect_files`.
2.  Reads the content of each file into memory and stores it in the `all_contents` dictionary for use by the LLM. This pre-reading optimizes performance in a multithreaded context.
3.  Creates the output directory (`mkdocs_dir/docs_dir`) if it doesn't exist.
4.  Uses `ThreadPoolExecutor` to parallelize the call to `generate_docs` for each file.
5.  Writes the generated documentation to a Markdown file in the output directory, creating subdirectories as needed to mirror the input directory structure.
6.  Handles errors during file processing and documentation generation.

**Example:**

```python
# Assuming core_instance is an instance of MeowdocCore
generated_files = core_instance.process_path()
if generated_files:
    print("Generated documentation files:")
    for file_path in generated_files:
        print(file_path)
else:
    print("No documentation files were generated.")
```

### `process_docguide_pages` Method

```python
def process_docguide_pages(self):
```

Processes files within the `docguide/(pages)` directory to create documentation pages.  It handles both `.md` files (which are simply copied) and `.ai.md` files (which contain prompts for the LLM). It uses a thread pool to parallelize processing pages, improving performance.

**Returns:**

*   `list[str]`: A list of relative paths (relative to `docs_dir`) of the processed pages. This list is used to update the MkDocs navigation.  Returns an empty list if the `docguide/(pages)` directory does not exist.

**Functionality:**

1.  Checks for the existence of the `docguide/(pages)` directory.  If it doesn't exist, it returns an empty list.
2.  Traverses the directory and identifies `.md` and `.ai.md` files.
3.  For `.md` files, copies them directly to the output directory (`mkdocs_dir/docs_dir`).
4.  For `.ai.md` files, treats the file content as a prompt for the LLM, generates content, and writes the result to a corresponding `.md` file in the output directory.
5.  Uses `ThreadPoolExecutor` to parallelize the processing of each page.

**Example:**

```python
# Assuming core_instance is an instance of MeowdocCore
page_relative_paths = core_instance.process_docguide_pages()
if page_relative_paths:
    print("Processed docguide pages:")
    for path in page_relative_paths:
        print(path)
else:
    print("No docguide pages were processed.")
```

### `_process_single_docguide_page` Method

```python
def _process_single_docguide_page(self, input_filepath, output_filepath, relative_output_path_for_nav, use_ai):
```

A helper function used by `process_docguide_pages` to process a single docguide page.  Handles both copying `.md` files and generating content from `.ai.md` files.

**Parameters:**

*   `input_filepath` (str): The absolute path to the input file (`.md` or `.ai.md`).
*   `output_filepath` (str): The absolute path to the output file (always `.md`).
*   `relative_output_path_for_nav` (str): The relative path (relative to `docs_dir`) of the output file.  This is the value that is returned if processing is successful.
*   `use_ai` (bool): `True` if the file is a `.ai.md` file and requires LLM generation, `False` if it's a `.md` file and should simply be copied.

**Returns:**

*   `str`: The `relative_output_path_for_nav` if processing is successful.
*   `None`: If an error occurs during processing.

**Functionality:**

1.  Creates the output directory if it doesn't exist.
2.  If `use_ai` is `True`:
    *   Reads the content of the input file as a prompt.
    *   Calls the LLM to generate content.
    *   Writes the generated content to the output file.
3.  If `use_ai` is `False`:
    *   Copies the input file to the output file.

**Example:**

This method is called internally by `process_docguide_pages` and is not intended to be called directly.

### `create_project_index` Method

```python
def create_project_index(self):
```

Creates the `index.md` file in the `docs_dir` directory, which serves as the main landing page for the documentation.  The content of the index file includes the project name, a description, a "Getting Started" section with installation instructions, a "Contributing" section generated by the LLM, license information, and a link to the repository.

**Functionality:**

1.  Uses the `project_name` and `project_description` from the `MeowdocCore` instance.
2.  Generates a "Contributing" section using the LLM, providing it with the project name to tailor the content.
3.  Constructs the complete content of the `index.md` file.
4.  Writes the content to the `index.md` file in the `docs_dir` directory.

**Example:**

```python
# Assuming core_instance is an instance of MeowdocCore
core_instance.create_project_index()
print("Project index created successfully.")
```

## Interaction with Other Modules

*   **`llm.py`:** The `MeowdocCore` class relies on the `llm.py` module to interact with the LLM.  It uses an `LLMProvider` instance (e.g., `GeminiProvider`, `OpenAiProvider`, or `OllamaProvider`) to generate documentation from prompts.  The `get_llm_provider` function in `llm.py` is used to instantiate the appropriate provider based on the configuration.
*   **`mkdocs.py`:** The `MeowdocCore` class interacts with the `mkdocs.py` module to manage the MkDocs project. It leverages functions like `update_mkdocs_nav` and `update_mkdocs_config_from_toml` to update the MkDocs configuration file (`mkdocs.yml`) with the generated documentation structure and any additional settings from the configuration file. `create_mkdocs_project` is used to create the project if one does not yet exist.
*   **`cli.py`:** The `cli.py` module uses the `MeowdocCore` class to drive the entire documentation generation process. It parses command-line arguments, loads the configuration, initializes the `MeowdocCore` instance, and calls its methods to generate the documentation and update the MkDocs project.

## Example Usage

See the `cli.py` file for an example of how to instantiate and use the `MeowdocCore` class.  The `cli.py` module handles command-line arguments and configuration loading to set up the `MeowdocCore` instance with the appropriate parameters.

```python
# This is example of using the MeowdocCore, more details can be found in `cli.py`

from meowdoc import core, llm

# Configuration loading and LLM provider instantiation would happen here in a real application

# Example configuration (replace with your actual config)
config = {
    "main": {
        "input_path": "src",
        "mkdocs_dir": "mkdocs",
        "docs_dir_name": "docs",
    },
    "ignore": {
        "patterns": [".venv", "*.pyc"]
    },
    "project": {
        "name": "MyProject",
        "description": "A sample project",
        "repo_url": "https://github.com/example/myproject"
    },
    "llm": {
        "provider": "gemini",
        "api_key_file": "path/to/your/api_key.txt",
        "model": "gemini-pro"
    }
}

# Instantiate the LLM provider
llm_provider = llm.get_llm_provider(config)

# Instantiate the MeowdocCore
generator = core.MeowdocCore(
    input_path=config["main"]["input_path"],
    mkdocs_dir=config["main"]["mkdocs_dir"],
    docs_dir=config["main"]["docs_dir_name"],
    ignore_patterns=config["ignore"]["patterns"],
    project_name=config["project"]["name"],
    project_description=config["project"]["description"],
    repo_url=config["project"]["repo_url"],
    llm_provider=llm_provider
)

# Process the input path and generate documentation
generated_files = generator.process_path()

if generated_files:
    print("Generated documentation files:")
    for file_path in generated_files:
        print(file_path)
else:
    print("No documentation files were generated.")

```
