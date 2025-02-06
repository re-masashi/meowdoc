```markdown
# `mkdocs.py` Module Documentation

This module provides functions to create and update MkDocs projects. It handles the creation of a new MkDocs project, updating the `mkdocs.yml` configuration file, and enabling specified themes. It interacts with the `meowdoc` library for theme management and uses `yaml` for configuration file manipulation.

## Module Overview

The primary purpose of this module is to automate the setup and configuration of MkDocs projects. It simplifies the process of integrating generated documentation into an existing or new MkDocs project. The module offers two main functionalities: creating a new MkDocs project and updating an existing one with new navigation entries.

## Functions

### `update_mkdocs_nav(generated_files, is_input_dir, mkdocs_dir, docs_dir_name, name, description, theme="material")`

Updates the `mkdocs.yml` file with navigation links to the generated documentation files.

#### Parameters:

*   `generated_files` (list): A list of file paths for which navigation links need to be added.
*   `is_input_dir` (bool): Indicates whether the input was a directory or a single file. If True, it handles nested directory structures within the documentation.
*   `mkdocs_dir` (str): The path to the MkDocs project directory.
*   `docs_dir_name` (str): The name of the documentation directory within the MkDocs project (e.g., "docs").
*   `name` (str): The name of the MkDocs site (used for `site_name` in `mkdocs.yml`).
*   `description` (str): The description of the MkDocs site (not currently used).
*   `theme` (str, optional): The theme to apply to the MkDocs site. Defaults to "material". This value is looked up in the `meowdoc.themes.THEMES` dictionary.

#### Functionality:

1.  **Loads `mkdocs.yml`:** Attempts to load the `mkdocs.yml` file using `yaml.safe_load`. Handles `FileNotFoundError` and `yaml.YAMLError` exceptions with appropriate logging.
2.  **Configures Basic Settings:** Sets the `site_name` and `theme` in the `mkdocs.yml` configuration. The theme name is retrieved from `meowdoc.themes.THEMES` based on the `theme` parameter.
3.  **Handles Navigation:**
    *   If `is_input_dir` is True:
        *   It creates a nested navigation structure based on the directory structure of the generated files.
        *   The navigation is added under an "API" section within the `mkdocs.yml` file.
        *   It utilizes a recursive function, `convert_to_mkdocs_nav`, to convert a nested dictionary representing the file structure into the list of dictionaries structure that MkDocs expects for its `nav`.
    *   If `is_input_dir` is False (single file):
        *   It creates a simple navigation entry for the single generated file.
4.  **Writes to `mkdocs.yml`:** Writes the updated `mkdocs_config` back to the `mkdocs.yml` file, using `yaml.dump` with indentation for readability. Handles potential exceptions during file writing.
5.  **Enables Theme:** Calls `themes.enable_theme` to perform any theme-specific setup.

#### Interactions:

*   Reads and writes the `mkdocs.yml` file.
*   Uses the `meowdoc.themes` module to enable the specified theme.
*   Relies on the provided `generated_files` list to create the navigation structure.

#### Example Usage:

```python
generated_files = ["docs/module1.md", "docs/package/module2.md"]
update_mkdocs_nav(
    generated_files,
    True,
    "my_project",
    "docs",
    "My Project",
    "A project description",
    theme="material",
)
```

### `create_mkdocs_project(project_dir, docs_dir_name)`

Creates a new MkDocs project in the specified directory if one doesn't already exist.

#### Parameters:

*   `project_dir` (str): The directory where the MkDocs project should be created.
*   `docs_dir_name` (str): The name of the documentation directory that will be created inside the project (often "docs").

#### Functionality:

1.  **Checks for Existing Project:** Determines if a `mkdocs.yml` file already exists in the specified directory.
2.  **Creates New Project (if necessary):**
    *   If no existing project is found, it uses the `mkdocs new` command to create a new MkDocs project in the specified directory.
    *   It uses `subprocess.run` to execute the `mkdocs new` command. The `check=True` argument ensures that an exception is raised if the command fails.  `capture_output=True` and `text=True` capture stdout and stderr for logging.
    *   Adds a default "Home" navigation entry to the `mkdocs.yml`.
3.  **Logs Information:** Logs messages indicating whether a new project was created or if one already exists.

#### Interactions:

*   Executes the `mkdocs` command-line tool via `subprocess`.
*   Creates a `mkdocs.yml` file with a default "Home" entry if it doesn't exist.

#### Example Usage:

```python
create_mkdocs_project("my_project", "docs")
```

## Usage Examples

### Creating a New MkDocs Project and Updating Navigation

```python
from mkdocs import create_mkdocs_project, update_mkdocs_nav
import os

# Create a new MkDocs project if it doesn't exist
project_dir = "my_project"
docs_dir_name = "docs"
create_mkdocs_project(project_dir, docs_dir_name)

# Example generated documentation files
generated_files = [
    os.path.join(project_dir, docs_dir_name, "module1.md"),
    os.path.join(project_dir, docs_dir_name, "package", "module2.md"),
]

# Update the mkdocs.yml file with navigation links
update_mkdocs_nav(
    generated_files,
    True,  # is_input_dir
    project_dir,
    docs_dir_name,
    "My Project",
    "A project to document.",
    theme="material",
)
```

## Dependencies

*   `os`: For file path manipulation.
*   `logging`: For logging information, errors, and warnings.
*   `yaml`: For reading and writing `mkdocs.yml` configuration files.
*   `subprocess`: For running the `mkdocs` command-line tool.
*   `meowdoc.themes`: For enabling and managing MkDocs themes.

## Notes

*   Error handling is implemented to catch common issues such as missing `mkdocs.yml` files or YAML parsing errors.
*   The module assumes that the `mkdocs` command-line tool is installed and available in the system's PATH.
*   The `meowdoc` themes need to be configured properly for the `themes.enable_theme` function to work as expected.
*   When `is_input_dir` is True, the generated navigation structure mirrors the directory structure of the input files. This is useful for documenting projects with multiple modules and packages.
*   The module uses relative paths for navigation links in `mkdocs.yml`, making the documentation portable.

## Integration with `core.py`

The `mkdocs.py` module is integrated with the `core.py` module as follows:

1.  The `MeowdocCore` class in `core.py` uses the `mkdocs_dir` and `docs_dir` attributes to determine where the MkDocs project is located and where the documentation files should be placed.
2.  After the documentation files are generated by the LLM and saved to the `docs_dir`, the `update_mkdocs_nav` function from `mkdocs.py` is called to update the `mkdocs.yml` file with the new documentation files. This ensures that the generated documentation is properly linked in the MkDocs navigation.
3.  `create_mkdocs_project` can be used in `core.py` to create the initial mkdocs project if it doesn't exist.

The `MeowdocCore` class initializes `mkdocs_dir` and `docs_dir` and likely calls the functions within `mkdocs.py` after generating the documentation markdown files.  The `project_name`, `project_description` and `repo_url` parameters in `MeowdocCore` are also leveraged by `mkdocs.py` to customize the mkdocs project.
```