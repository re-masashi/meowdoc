# `mkdocs.py` Documentation

This module provides functions to create, update, and finalize MkDocs projects for documentation generation. It handles MkDocs project setup, navigation updates based on generated documentation files, and configuration adjustments. The module interacts with `yaml` for reading and writing MkDocs configuration files (`mkdocs.yml`), `subprocess` for running MkDocs commands, and the `meowdoc.themes` module for managing MkDocs themes. It aims to automate the integration of generated documentation into a MkDocs project.

## Module-Level Description

The `mkdocs.py` module contains functions for managing MkDocs projects. These functions facilitate the creation of new MkDocs projects, updating the navigation structure based on generated documentation files, merging configurations from TOML files, deduplicating YAML keys, and enabling specific themes.  It simplifies the process of maintaining a MkDocs documentation site for a Python project.

## Functions

### `update_mkdocs_nav(generated_files, is_input_dir, mkdocs_dir, docs_dir_name, name, description, theme="material")`

Updates the `mkdocs.yml` file with navigation links to the generated documentation files. It can handle both single files and directories of files, creating a nested navigation structure for directories.

#### Parameters

*   `generated_files` (list): A list of file paths to the generated Markdown documentation files.
*   `is_input_dir` (bool): A boolean indicating whether the input was a directory.  If `True`, the function generates a nested navigation structure for the files within the directory. If `False`, it handles a single file.
*   `mkdocs_dir` (str): The path to the MkDocs project directory.
*   `docs_dir_name` (str): The name of the directory within the MkDocs project where the documentation files are stored (e.g., "docs").
*   `name` (str): The name of the project, which will be used as the `site_name` in `mkdocs.yml`.
*   `description` (str): The description of the project (not currently used).
*   `theme` (str, optional): The MkDocs theme to use. Defaults to "material".

#### Functionality

1.  **Loads `mkdocs.yml`:** Reads the `mkdocs.yml` file from the specified `mkdocs_dir`.  Handles `FileNotFoundError` and `yaml.YAMLError` if the file doesn't exist or is invalid.
2.  **Sets `site_name` and `theme`:**  Updates the `site_name` and `theme` entries in the `mkdocs.yml` dictionary.  The theme uses the `themes.THEMES` dictionary to map a simplified theme name (e.g., "material") to the appropriate MkDocs theme name (e.g., "material").
3.  **Updates Navigation:**
    *   If `is_input_dir` is `True`, the function creates a nested navigation structure based on the directory structure of the `generated_files`. It ensures the API section exists, creating one if it doesn't. The function builds a nested dictionary representing the directory structure and converts it to the format expected by MkDocs for the `nav` section.
    *   If `is_input_dir` is `False`, the function adds a simple navigation entry for the single `generated_files` entry, creating a nav entry pointing directly to the file.
4.  **Writes `mkdocs.yml`:** Writes the updated `mkdocs_config` back to the `mkdocs.yml` file, using an indent of 2 for better readability. Handles potential exceptions during file writing.
5.  **Enables Theme:** Calls `themes.enable_theme()` to install and potentially configure the selected MkDocs theme.

#### Example

```python
generated_files = ["docs/module1.md", "docs/module2.md"]
update_mkdocs_nav(
    generated_files,
    False,
    "my_mkdocs_project",
    "docs",
    "My Project",
    "A sample project.",
    theme="material",
)
```

#### Interactions with other modules

*   **yaml:** For reading and writing the `mkdocs.yml` configuration file.
*   **os:** For path manipulation and checking file existence.
*   **logging:** For logging information and errors.
*   **meowdoc.themes:** For enabling the specified MkDocs theme.

### `create_mkdocs_project(project_dir, docs_dir_name)`

Creates a new MkDocs project in the specified directory if one doesn't already exist.

#### Parameters

*   `project_dir` (str): The directory where the MkDocs project should be created.
*    `docs_dir_name` (str): The directory to hold documentation files

#### Functionality

1.  **Checks for Existing Project:** Checks if a `mkdocs.yml` file already exists in the `project_dir`.
2.  **Creates Project:** If a `mkdocs.yml` file doesn't exist, it runs the `mkdocs new` command using `subprocess` to create a new MkDocs project in the `project_dir`.
3.  **Adds Default Navigation:** Adds a default `nav` entry with a "Home" link to the `index.md` file in the newly created `mkdocs.yml` file.
4.  **Handles Errors:** Catches `subprocess.CalledProcessError` if the `mkdocs new` command fails and logs the error, stdout, and stderr.  Also catches general exceptions.
5. Returns `True` if a new project was created, `False` on error. Returns `True` if a project already exists.

#### Example

```python
create_mkdocs_project("my_mkdocs_project", "docs")
```

#### Interactions with other modules

*   **os:** For path manipulation and checking file existence.
*   **subprocess:** For running the `mkdocs new` command.
*   **logging:** For logging information and errors.
*   **yaml:** For modifying the default navigation after project creation.

### `merge_dicts(existing, new)`

Recursively merges two dictionaries.  Values from the `new` dictionary overwrite values in the `existing` dictionary, but nested dictionaries are merged recursively.

#### Parameters

*   `existing` (dict): The existing dictionary to merge into. This dictionary is modified in place.
*   `new` (dict): The new dictionary to merge from.

#### Functionality

1.  **Iterates Through New Dictionary:** Loops through the key-value pairs in the `new` dictionary.
2.  **Handles Nested Dictionaries:** If a value in the `new` dictionary is a dictionary and the corresponding key exists in the `existing` dictionary and its value is also a dictionary, the function recursively calls itself to merge the nested dictionaries.
3.  **Overwrites or Adds Values:** Otherwise, the value from the `new` dictionary is assigned to the corresponding key in the `existing` dictionary, overwriting any existing value or adding the key-value pair if it doesn't exist.
4.  Returns the `existing` dictionary, which has been modified.

#### Example

```python
existing_dict = {"a": 1, "b": {"c": 2, "d": 3}}
new_dict = {"b": {"c": 4, "e": 5}, "f": 6}
merged_dict = merge_dicts(existing_dict, new_dict)
print(merged_dict)  # Output: {'a': 1, 'b': {'c': 4, 'd': 3, 'e': 5}, 'f': 6}
```

#### Interactions with other modules

None.

### `dedupe_yaml_keep_last(yaml_str)`

Deduplicates keys in a YAML string, keeping only the last occurrence of each key.

#### Parameters

*   `yaml_str` (str): The YAML string to deduplicate.

#### Functionality

1.  **Custom YAML Loader:** Defines a custom YAML loader (`LastKeyLoader`) that uses an `OrderedDict` to load the YAML data.  The `construct_mapping` function in the loader overwrites the value of a key if it already exists in the `OrderedDict`, effectively keeping only the last occurrence.
2.  **Loads YAML:** Loads the YAML string using the custom `LastKeyLoader`.
3.  **Dumps YAML:** Dumps the loaded data back into a YAML string, preserving the order from the `OrderedDict` using `sort_keys=False`.

#### Example

```python
yaml_string = """
a: 1
b: 2
a: 3
c: 4
b: 5
"""
deduplicated_yaml = dedupe_yaml_keep_last(yaml_string)
print(deduplicated_yaml)
# Expected output (order may vary):
# a: 3
# b: 5
# c: 4
```

#### Interactions with other modules

*   **yaml:** For loading and dumping YAML data.
*   **collections.OrderedDict:** For preserving the order of keys during YAML loading.

### `finalize(mkdocs_dir)`

Finalizes the `mkdocs.yml` file by deduplicating keys, ensuring only the last occurrence of each key is kept.

#### Parameters

*   `mkdocs_dir` (str): The path to the MkDocs project directory.

#### Functionality

1.  **Reads `mkdocs.yml`:** Reads the content of `mkdocs.yml` file.
2.  **Deduplicates YAML:** Calls the `dedupe_yaml_keep_last` function to deduplicate the keys in the YAML string.
3.  **Writes `mkdocs.yml`:** Writes the deduplicated YAML string back to the `mkdocs.yml` file. Handles exceptions during file writing.

#### Example

```python
finalize("my_mkdocs_project")
```

#### Interactions with other modules

*   **os:** For path manipulation.
*   **logging:** For logging information and errors.
*   **yaml:** For reading and writing the `mkdocs.yml` file and deduplicating the keys.

### `update_mkdocs_config_from_toml(config, mkdocs_dir)`

Updates the `mkdocs.yml` file with settings from a TOML configuration file.

#### Parameters

*   `config` (dict): A dictionary representing the TOML configuration.  It expects a `"mkdocs"` section containing the settings to be merged into `mkdocs.yml`.
*   `mkdocs_dir` (str): The path to the MkDocs project directory.

#### Functionality

1.  **Loads MkDocs Settings from TOML:** Extracts the `"mkdocs"` section from the `config` dictionary.  If the `"mkdocs"` section is not present, an empty dictionary is used.
2.  **Loads `mkdocs.yml`:** Reads the `mkdocs.yml` file.  Handles `FileNotFoundError` and `yaml.YAMLError` if the file doesn't exist or is invalid.
3.  **Merges Configurations:** Calls the `merge_dicts` function to merge the settings from the TOML file into the `mkdocs_config` dictionary.
4.  **Writes `mkdocs.yml`:** Writes the updated `mkdocs_config` back to the `mkdocs.yml` file, using an indent of 2 for better readability. Handles exceptions during file writing.

#### Example

```python
config = {
    "mkdocs": {
        "site_name": "My Updated Project",
        "theme": {"name": "readthedocs"},
    }
}
update_mkdocs_config_from_toml(config, "my_mkdocs_project")
```

#### Interactions with other modules

*   **os:** For path manipulation.
*   **logging:** For logging information and errors.
*   **yaml:** For reading and writing the `mkdocs.yml` file.
*   `merge_dicts`: For merging dictionaries

## Integration with other modules

This module is closely integrated with other parts of the Meowdoc documentation generation process.

*   **`core.py` (MeowdocCore):** The `update_mkdocs_nav`, `create_mkdocs_project`, `update_mkdocs_config_from_toml` and `finalize` functions are called by the `MeowdocCore` class after the documentation files have been generated.  `MeowdocCore` provides the list of generated files, project name, and other configuration information needed to update the MkDocs project. The `MeowdocCore` class uses the functions to create the basic mkdocs setup, add all generated files to the navigation, updates the basic config and cleans the generated config from duplicated entries.
*   **`cli.py`:** The command-line interface calls the functions in this module to create the MkDocs project and update its configuration based on the command-line arguments and configuration file. It orchestrates the entire documentation generation process. It makes sure, the mkdocs project is setup, before calling the core module to generate content.
*   **`themes.py`:** The `update_mkdocs_nav` calls the `themes.enable_theme` function to configure the MkDocs theme.

## MkDocs Definition

MkDocs is a fast, simple and downright gorgeous static site generator that's geared towards building project documentation. Documentation source files are written in Markdown, and configured with a single YAML configuration file. MkDocs is often used to present documentation for projects in a clean and easily navigable format.
