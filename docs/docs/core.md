# `core.py` Documentation

This module defines the `MeowdocCore` class, which is the core component for generating documentation for Python projects using a Large Language Model (LLM) and MkDocs.  It handles file processing, interaction with the LLM, and the creation of Markdown files for the documentation.

## Module Contents

### `MeowdocCore` Class

The `MeowdocCore` class orchestrates the documentation generation process.  It takes a project's source code, uses an LLM to generate documentation, and then structures that documentation into Markdown files suitable for use with MkDocs.

```python
class MeowdocCore:
    """A class to generate documentation for Python files using LLM and MkDocs."""
```

#### `__init__(self, input_path, mkdocs_dir, docs_dir, ignore_patterns, project_name, project_description, repo_url, llm_provider)`

Initializes the `MeowdocCore` instance. This involves setting up the paths for input, MkDocs configuration, and output documentation, as well as configuring ignore patterns, project metadata, and the LLM provider.

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

**Parameters:**

*   `input_path` (str): The path to the directory containing the Python source code, or a path to a specific file. This is the code to be documented.
*   `mkdocs_dir` (str): The path to the root directory of the MkDocs project.
*   `docs_dir` (str): The name of the directory within the MkDocs project where the generated Markdown documentation will be placed.  This is relative to `mkdocs_dir`.
*   `ignore_patterns` (list of str): A list of filename patterns to ignore during documentation generation. These patterns use `fnmatch` syntax (e.g., `*.pyc`, `__init__.py`).
*   `project_name` (str): The name of the project.  Used in the generated `index.md` file.
*   `project_description` (str): A short description of the project.  Used in the generated `index.md` file.
*   `repo_url` (str): The URL of the project's repository (e.g., GitHub).
*   `llm_provider` (object): An object that provides an interface to a Large Language Model (LLM). This object must have a `generate` method that accepts a prompt string and returns a string containing the LLM's response.  The specific implementation of this object will depend on the LLM being used.

**Example:**

```python
# Assuming you have an LLM provider class called 'MyLLMProvider'
# and a project directory structure.
from core import MeowdocCore

# Initialize the documentation generator
doc_generator = MeowdocCore(
    input_path="my_project",
    mkdocs_dir="mkdocs",
    docs_dir="docs",
    ignore_patterns=["*.pyc", "__init__.py"],
    project_name="MyProject",
    project_description="A simple example project.",
    repo_url="https://github.com/example/myproject",
    llm_provider=MyLLMProvider()
)
```

#### `generate_docs(self, file_path, all_file_contents)`

Generates documentation for a single Python file using the LLM.  The LLM is provided with the content of the file to be documented, as well as the contents of all other files in the project to provide context.

```python
    def generate_docs(self, file_path, all_file_contents):
        """Generates documentation for a single file with context from all related files."""
```

**Parameters:**

*   `file_path` (str): The path to the Python file to generate documentation for.
*   `all_file_contents` (dict): A dictionary where keys are filenames (relative to the input path specified in the constructor) and values are the contents of the corresponding files.  This allows the LLM to understand the context of the file being documented.

**Returns:**

*   str: The generated documentation in Markdown format, or `None` if an error occurred.

**Details:**

This method constructs a prompt for the LLM that includes the file content to be documented and the content of all other files in the project for context.  It then calls the `generate` method of the `llm_provider` to get the LLM's response, which should be the documentation in Markdown format. The file name stored in all_file_contents is a relative path to the input directory.

**Example:**

```python
# Assuming doc_generator is an instance of MeowdocCore,
# file_path is the path to a Python file, and
# all_file_contents is a dictionary of file contents.

markdown_docs = doc_generator.generate_docs(file_path, all_file_contents)

if markdown_docs:
    print(markdown_docs)  # Output the generated Markdown documentation
else:
    print("Failed to generate documentation.")
```

#### `create_index(self, mkdocs_dir, docs_dir, readme_content)`

Creates the `index.md` file within the MkDocs documentation directory, using the provided content (typically the project's README file).  This serves as the main landing page for the documentation.

```python
    def create_index(self, mkdocs_dir, docs_dir, readme_content):
        """Creates the index.md file with the provided content."""
```

**Parameters:**

*   `mkdocs_dir` (str): The path to the root directory of the MkDocs project.
*   `docs_dir` (str): The name of the directory within the MkDocs project where the generated Markdown documentation will be placed. This is relative to `mkdocs_dir`.
*   `readme_content` (str): The content to write to the `index.md` file.  This is often the content of the project's README file.

**Example:**

```python
# Assuming doc_generator is an instance of MeowdocCore,
# mkdocs_dir and docs_dir are configured correctly, and
# readme_content contains the content of the README file.

with open("README.md", "r", encoding="utf-8") as f:
    readme_content = f.read()

doc_generator.create_index(
    mkdocs_dir="mkdocs",
    docs_dir="docs",
    readme_content=readme_content
)
```

#### `should_ignore(self, path, ignore_patterns)`

Determines whether a given file or directory path should be ignored based on the configured `ignore_patterns`.  It checks not only the path itself but also all of its parent directories to prevent processing files within ignored directories.

```python
    def should_ignore(self, path, ignore_patterns):
        """Checks if a path or any of its parent directories should be ignored."""
```

**Parameters:**

*   `path` (str): The path to check.
*   `ignore_patterns` (list of str): A list of filename patterns to ignore.  These patterns use `fnmatch` syntax (e.g., `*.pyc`, `__init__.py`).

**Returns:**

*   bool: `True` if the path or any of its parent directories should be ignored, `False` otherwise.

**Details:**

This method converts the input path to an absolute path for consistent comparisons.  It then iteratively checks the path and each of its parent directories against the `ignore_patterns`.

**Example:**

```python
# Assuming doc_generator is an instance of MeowdocCore,
# path is the path to a file or directory, and
# ignore_patterns is a list of patterns to ignore.

if doc_generator.should_ignore(path="my_project/ignore_me.py", ignore_patterns=["ignore_me.py"]):
    print("Ignoring the path.")
else:
    print("Processing the path.")

if doc_generator.should_ignore(path="my_project/.hidden/important.py", ignore_patterns=[".hidden"]):
    print("Ignoring the path.")
else:
    print("Processing the path.")
```

#### `process_path(self, input_path=None)`

Processes the input path, which can be either a single file or a directory.  If it's a directory, it recursively walks through the directory structure, generating documentation for each Python file.  It respects the configured `ignore_patterns` and ensures that the MkDocs directory itself is not processed.

```python
    def process_path(self, input_path=None):
```

**Parameters:**

*   `input_path` (str, optional): The path to process. If `None`, it defaults to the `input_path` specified in the constructor.

**Returns:**

*   list of str: A list of paths to the generated Markdown files.

**Details:**

This method is the main entry point for documentation generation. It handles the logic for traversing the input path (whether it's a file or a directory), reading file contents, calling the `generate_docs` method to generate the documentation, and writing the documentation to Markdown files in the output directory. The filenames in the all_file_contents dict are stored as relative paths to the input directory.

**Example:**

```python
# Assuming doc_generator is an instance of MeowdocCore and is properly initialized.

generated_files = doc_generator.process_path()

if generated_files:
    print("Generated files:")
    for file in generated_files:
        print(file)
else:
    print("No files were generated.")
```

#### `create_project_index(self)`

Creates the project's main `index.md` file, which serves as the landing page for the documentation.  This includes the project name, a description, installation instructions, contributing guidelines (generated by the LLM), and license information.

```python
    def create_project_index(
        self,
    ):
```

**Parameters:**

*   None

**Returns:**

*   None

**Details:**

This method uses the LLM to generate a "Contributing" section for the index page.  It then constructs the complete `index.md` content with the project name, description, installation instructions, the generated "Contributing" section, and license/repository information.  Finally, it writes the content to the `index.md` file in the appropriate directory.

**Example:**

```python
# Assuming doc_generator is an instance of MeowdocCore and is properly initialized.

doc_generator.create_project_index()
```

## Interaction with Other Modules

*   **LLM Provider:** The `MeowdocCore` class depends on an external LLM provider, which is passed as the `llm_provider` argument to the constructor. This provider must have a `generate` method that accepts a text prompt and returns a string response.  The specifics of the LLM provider are not defined within this module, allowing for flexibility in choosing the LLM.

*   **Operating System:** The `os` module is used for interacting with the file system, such as creating directories, walking through directory trees, and reading file contents.

*   **Logging:**  The `logging` module is used to log information, warnings, and errors during the documentation generation process.

*   **`fnmatch`:** Used for matching filenames against ignore patterns.

*   **`pathlib`:**  Used for creating directories, including parent directories, in a platform-independent way.

##  Example Usage

A typical workflow involves the following steps:

1.  **Initialization:** Create an instance of the `MeowdocCore` class, providing the necessary configuration parameters, including a LLM provider.

2.  **Process Path:** Call the `process_path` method to start the documentation generation process, specifying the root directory of the Python project.

3.  **Create Index:** Call the `create_index` method to create the project's `index.md` file, using the project's README content (or a custom index page).  Alternatively, call the `create_project_index` method to create an AI generated project index.

## Error Handling

The `MeowdocCore` class includes error handling to gracefully handle potential issues during the documentation generation process:

*   **File Reading Errors:**  If a file cannot be read, a logging error is generated, and the process continues to the next file.
*   **LLM Errors:**  If the LLM API call fails, a logging exception is generated, and `None` is returned (which is handled by the calling function).
*   **Invalid Paths:**  If the specified input path is invalid, a logging warning is generated, and the path is skipped.

## Future Enhancements

*   **More sophisticated prompting:** Implement more sophisticated prompting strategies to improve the quality and accuracy of the generated documentation. This could involve providing more context to the LLM, such as dependency information or code execution examples.
*   **Customizable output format:** Allow users to customize the output format of the generated documentation.
*   **Integration with other documentation tools:** Integrate with other documentation tools, such as Sphinx, to provide a more comprehensive documentation solution.
