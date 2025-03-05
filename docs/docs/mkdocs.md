# Module: `mkdocs.py`

This module provides functions for creating and updating MkDocs projects and their configurations, specifically focusing on integrating generated documentation into the MkDocs navigation structure. It interacts with the `meowdoc.themes` module to enable specified themes.

## Functions

### `update_mkdocs_nav(generated_files, is_input_dir, mkdocs_dir, docs_dir_name, name, description, theme="material")`

Updates the `mkdocs.yml` file of an MkDocs project to include generated documentation files in the navigation.

**Parameters:**

*   `generated_files` (list): A list of file paths to the generated documentation files (Markdown files).
*   `is_input_dir` (bool): A boolean indicating whether the input was a directory or a single file. If `True`, the function handles multiple files and creates a nested navigation structure. If `False`, it handles a single file.
*   `mkdocs_dir` (str): The path to the MkDocs project directory (where `mkdocs.yml` is located).
*   `docs_dir_name` (str): The name of the directory where the documentation files are stored within the MkDocs project (e.g., "docs").
*   `name` (str): The name of the MkDocs site (used as `site_name` in `mkdocs.yml`).
*   `description` (str):  Unused in the current implementation.  Intended as a project description.
*   `theme` (str, optional): The name of the MkDocs theme to use. Defaults to "material". This value must be a key in the `meowdoc.themes.THEMES` dictionary.

**Functionality:**

1.  **Loads `mkdocs.yml`:** Reads the existing `mkdocs.yml` file into a Python dictionary using `yaml.safe_load()`. Handles `FileNotFoundError` and `yaml.YAMLError` exceptions.
2.  **Sets Site Name and Theme:** Updates the `site_name` and `theme` keys in the `mkdocs.yml` dictionary. The theme name is retrieved from `themes.THEMES[theme]["mkdocs_name"]`, which converts the `theme` to the format understood by `mkdocs`.
3.  **Updates Navigation:**
    *   If `is_input_dir` is `True` (directory input):
        *   It checks if an "API" section already exists in the navigation. If not, it creates one.
        *   It builds a nested dictionary `file_nav_structure` representing the directory structure of the generated documentation files.  This dictionary is keyed by the directory and file names, with values being the relative paths to the files.
        *   A helper function `convert_to_mkdocs_nav` converts the nested dictionary into a list of dictionaries in the format expected by MkDocs for the navigation.
        *   Extends the `api_section` with the generated navigation structure.
    *   If `is_input_dir` is `False` (single file input):
        *   It creates a simple navigation entry with the filename as the title and the relative path to the file as the link.
        *   Appends this entry to the `nav` list in `mkdocs.yml`.
4.  **Writes Updated `mkdocs.yml`:** Writes the updated `mkdocs.yml` dictionary back to the file using `yaml.dump()`.
5.  **Enables Theme:** Calls `themes.enable_theme(theme)` to perform any necessary setup for the specified theme.

**Interactions with other modules:**

*   **`meowdoc.themes`:**  Uses `themes.THEMES` to map the theme name, and calls `themes.enable_theme()` to enable the theme.
*   **`yaml`:** Used for loading and dumping the `mkdocs.yml` file.
*   **`os`:** Used for file path manipulation and checking file existence.
*   **`logging`:**  Used for logging informational, error, and exception messages.

**Example:**

```python
# Assuming generated_files = ["docs/api/module1.md", "docs/api/module2.md"]
update_mkdocs_nav(
    generated_files=["docs/api/module1.md", "docs/api/module2.md"],
    is_input_dir=True,
    mkdocs_dir="my_project",
    docs_dir_name="docs",
    name="My Project",
    description="A description of my project",
    theme="material",
)
```

This would update the `mkdocs.yml` file in the `my_project` directory, adding an "API" section to the navigation containing links to `module1.md` and `module2.md`. The theme would be set to "material".

### `create_mkdocs_project(project_dir, docs_dir_name)`

Creates a new MkDocs project in the specified directory if one does not already exist.

**Parameters:**

*   `project_dir` (str): The directory where the MkDocs project should be created.
*   `docs_dir_name` (str): The name of the documentation directory inside the MkDocs project.

**Functionality:**

1.  **Checks for Existing Project:** Checks if an `mkdocs.yml` file already exists in the `project_dir`.
2.  **Creates New Project (if necessary):**
    *   If `mkdocs.yml` doesn't exist, it uses `subprocess.run()` to execute the `mkdocs new <project_dir>` command.
    *   Captures the standard output and standard error of the command for logging.
    *   If the creation is successful, it opens the newly created `mkdocs.yml` file, loads its content, adds a default navigation entry `{"Home": "index.md"}`, and saves the updated configuration.
3.  **Logs Status:** Logs messages indicating whether a new project was created or an existing one was found.

**Returns:**

*   `bool`: Returns `True` if a project existed or was successfully created. Returns `False` if the project creation failed.

**Interactions with other modules:**

*   **`subprocess`:**  Used to execute the `mkdocs new` command.
*   **`yaml`:** Used for loading and dumping the `mkdocs.yml` file when creating a new project.
*   **`os`:** Used for file path manipulation and checking file existence.
*   **`logging`:** Used for logging informational, error, and exception messages.

**Example:**

```python
success = create_mkdocs_project("my_project", "docs")
if success:
    print("MkDocs project created or already exists.")
else:
    print("Failed to create MkDocs project.")
```

This would create a new MkDocs project in the `my_project` directory if one doesn't already exist.

## Interaction with other modules (based on the provided context)

*   **`core.py` (MeowdocCore):** The `mkdocs.py` module is called from `core.py` after the documentation files have been generated by the LLM.  Specifically, `update_mkdocs_nav` is likely called to update the `mkdocs.yml` file with the newly generated documentation. The `create_mkdocs_project` is likely called at the beginning of a project to initialise mkdocs.

*   **`themes.py` (meowdoc.themes):**  The `update_mkdocs_nav` function directly interacts with the `meowdoc.themes` module to configure the MkDocs theme. The `themes.THEMES` dictionary is used to look up the correct name for the theme in `mkdocs.yml`, and the `themes.enable_theme` function is called to apply the theme.

## Usage

The functions in this module are designed to be used within a larger documentation generation workflow, such as the one implemented by the `MeowdocCore` class in `core.py`. The general flow would be:

1.  Create a MkDocs project using `create_mkdocs_project()`.
2.  Generate documentation files for the Python code using an LLM (as done in `core.py`).
3.  Update the MkDocs navigation to include the generated documentation files using `update_mkdocs_nav()`.

This ensures that the generated documentation is properly integrated into the MkDocs site and can be easily accessed.
