# `mkdocs.py` Documentation

This module provides functions to manage and update MkDocs projects. It includes functionalities to create a new MkDocs project, update the `mkdocs.yml` configuration file, and handle navigation updates. It also supports merging configurations from a TOML file.

## Table of Contents

1.  [Dependencies](#dependencies)
2.  [Functions](#functions)
    *   [`update_mkdocs_nav`](#update_mkdocs_nav)
    *   [`create_mkdocs_project`](#create_mkdocs_project)
    *   [`merge_dicts`](#merge_dicts)
    *   [`finalize`](#finalize)
    *   [`_dedupe_API_elem`](#_dedupe_API_elem)
    *   [`update_mkdocs_config_from_toml`](#update_mkdocs_config_from_toml)

## Dependencies

This module relies on the following Python libraries:

*   `os`: For interacting with the operating system (e.g., file path manipulation).
*   `logging`: For logging messages and debugging information.
*   `yaml`: For reading and writing YAML configuration files.
*   `subprocess`: For running external commands (e.g., creating a new MkDocs project).
*   `meowdoc.themes`: For enabling themes in the MkDocs project. Specifically this file uses `themes.THEMES` for theme information and `themes.enable_theme` for enabling a theme.
*   `json`: For working with JSON data (used in deduplication).
*   `pprint`: For pretty printing Python data structures (used for debugging).
## Functions

### `update_mkdocs_nav`

```python
def update_mkdocs_nav(
    generated_files,
    page_relative_paths,
    is_input_dir,
    mkdocs_dir,
    docs_dir_name,
    name,
    description,
    theme="material",
):
```

Updates the `mkdocs.yml` file with the generated documentation files and project metadata, handling the navigation section.

**Parameters:**

*   `generated_files` (list): A list of paths to the generated Markdown files.
*   `page_relative_paths` (list): A list of relative paths for additional pages.
*   `is_input_dir` (bool): A boolean indicating whether the input path was a directory or a single file.
*   `mkdocs_dir` (str): The path to the MkDocs project directory.
*   `docs_dir_name` (str): The name of the documentation directory within the MkDocs project.
*   `name` (str): The name of the project.
*   `description` (str): The description of the project.
*   `theme` (str, optional): The theme to use for the MkDocs site. Defaults to "material".

**Functionality:**

1.  **Load Configuration:** Reads the existing `mkdocs.yml` file or creates a default configuration if it doesn't exist.
2.  **Update Metadata:** Sets the `site_name`, and `theme` in the `mkdocs.yml` file.
3.  **Update Navigation:**
    *   If `is_input_dir` is True (directory input):
        *   Constructs a nested navigation structure based on the directory structure of the generated files. An "API" section is created if it doesn't exist and new items are added to that "API" section. The path structure is extracted and added to the navigation tree.
    *   If `is_input_dir` is False (single file input):
        *   Adds the generated file to the navigation menu with the filename as the title.
    *   Adds any pages from the `page_relative_paths` that are not already in the navigation.
4.  **Write Configuration:** Writes the updated configuration back to the `mkdocs.yml` file.
5.  **Enable Theme:** Calls the `themes.enable_theme()` function to install and activate the specified theme.

**Error Handling:**

*   Logs an error if `mkdocs.yml` is not found.
*   Logs an error if there is an error parsing `mkdocs.yml`.
*   Logs an error if there is an error writing to `mkdocs.yml`.

**Example:**

```python
generated_files = ["docs/module1.md", "docs/module2.md"]
page_relative_paths = ["about.md"]
is_input_dir = True
mkdocs_dir = "my_project"
docs_dir_name = "docs"
name = "My Project"
description = "A sample project."
update_mkdocs_nav(generated_files, page_relative_paths, is_input_dir, mkdocs_dir, docs_dir_name, name, description)
```

### `create_mkdocs_project`

```python
def create_mkdocs_project(project_dir, docs_dir_name):
```

Creates a new MkDocs project in the specified directory if one does not already exist.

**Parameters:**

*   `project_dir` (str): The directory where the MkDocs project should be created.
*   `docs_dir_name` (str): The name of the documentation directory inside the MkDocs project.

**Functionality:**

1.  **Check for Existing Project:** Checks if an `mkdocs.yml` file already exists in the specified directory.
2.  **Create Project:** If no `mkdocs.yml` file exists, it uses the `mkdocs new` command to create a new MkDocs project.
3.  **Default Navigation:** Adds a default navigation entry ("Home": "index.md") to the newly created `mkdocs.yml` file.
4.  **Returns:** True if the project was created or already existed, False if creation failed.

**Error Handling:**

*   Logs an error if the `mkdocs new` command fails.

**Example:**

```python
project_dir = "my_project"
docs_dir_name = "docs"
create_mkdocs_project(project_dir, docs_dir_name)
```

### `merge_dicts`

```python
def merge_dicts(existing, new):
```

Recursively merges two dictionaries. Values from the `new` dictionary take precedence, but nested dictionaries are merged intelligently.

**Parameters:**

*   `existing` (dict): The existing dictionary to merge into.
*   `new` (dict): The new dictionary to merge from.

**Functionality:**

1.  **Iterate Through New Dictionary:** Iterates through each key-value pair in the `new` dictionary.
2.  **Handle Nested Dictionaries:** If a value in `new` is a dictionary and the corresponding value in `existing` is also a dictionary, it recursively calls `merge_dicts` to merge the nested dictionaries.
3.  **Overwrite or Add Values:** If a value in `new` is not a dictionary, or the corresponding value in `existing` is not a dictionary, the value from `new` overwrites the value in `existing`.
4.  **Returns:** The merged dictionary (the `existing` dictionary, modified in place).

**Example:**

```python
existing = {"a": 1, "b": {"c": 2, "d": 3}}
new = {"b": {"c": 4, "e": 5}, "f": 6}
merged = merge_dicts(existing, new)
# merged will be: {"a": 1, "b": {"c": 4, "d": 3, "e": 5}, "f": 6}
```

### `finalize`

```python
def finalize(mkdocs_config):
```

Finalizes the mkdocs config by deduplicating API elements.

**Parameters:**

*   `mkdocs_config` (dict): The mkdocs config to finalize

**Functionality:**

1.  If `mkdocs_config`'s `nav` attribute doesn't exist, it immediately returns the config.
2.  It maps each element in `mkdocs_config["nav"]` using the `_dedupe_API_elem` function, creating a new list `matches`.
3.  Finally, replaces the `nav` element with `matches`.

**Example:**

```python
mkdocs_config = {"nav": [{"API": [{"a": 1}, {"a": 1}, {"b": 2}]}]}
finalized_config = finalize(mkdocs_config)
# finalized_config will be: {'nav': [{'API': [{'a': 1}, {'b': 2}]}]}
```

### `_dedupe_API_elem`

```python
def _dedupe_API_elem(elem):
```

Helper function to deduplicate the elements in the API.

**Parameters:**

*   `elem` (dict): An element from the mkdocs navigation configuration.  This should be a dictionary that potentially contains an 'API' key with a list of dictionaries as its value.

**Functionality:**

1.  Check for an API key. If the current element `elem` does not contain the 'API' key, the function will return the element without modification.
2.  Convert and Check for Duplicates: Loop through each dictionary d in API, convert each dictionary to its JSON string representation (with keys sorted to ensure that dictionaries that may have different ordering but contain the same information are treated as equal), and only append the original dictionary d to the deduplicated_data list if its JSON string representation has not been seen before.
3.  Returns the modified element with the potentially deduplicated API section, or returns the original element if the API section wasn't present.

**Example:**

```python
elem = {"API": [{"a": 1}, {"a": 1}, {"b": 2}]}
deduped_elem = _dedupe_API_elem(elem)
# deduped_elem will be: {'API': [{'a': 1}, {'b': 2}]}
```

### `update_mkdocs_config_from_toml`

```python
def update_mkdocs_config_from_toml(config, mkdocs_dir):
```

Updates the `mkdocs.yml` file with settings from a TOML configuration file.

**Parameters:**

*   `config` (dict): A dictionary loaded from a TOML configuration file (likely `config.toml` in the calling CLI script).
*   `mkdocs_dir` (str): The path to the MkDocs project directory.

**Functionality:**

1.  **Load TOML Settings:** Extracts the `mkdocs` section from the provided TOML configuration dictionary.
2.  **Load Existing Configuration:** Loads the existing `mkdocs.yml` file.
3.  **Merge Configurations:** Merges the settings from the TOML configuration with the existing `mkdocs.yml` configuration, using the `merge_dicts` function.
4.  **Finalize configurations:** Deduplicates API elements
5.  **Write Updated Configuration:** Writes the updated configuration back to the `mkdocs.yml` file.

**Error Handling:**

*   Logs an error if `mkdocs.yml` is not found.
*   Logs an error if there is an error parsing `mkdocs.yml`.
*   Logs an error if there is an error writing to `mkdocs.yml`.

**Example:**

```python
config = {"mkdocs": {"site_name": "New Site Name", "theme": {"name": "readthedocs"}}}
mkdocs_dir = "my_project"
update_mkdocs_config_from_toml(config, mkdocs_dir)
```
