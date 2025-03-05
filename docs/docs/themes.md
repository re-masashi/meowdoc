# `themes.py` Module Documentation

This module defines a dictionary of available MkDocs themes and provides a function to enable a specific theme by installing the corresponding `pip` package. It interacts with the `mkdocs.py` module to update the `mkdocs.yml` configuration file with the selected theme.

## Module Overview

This module handles the management of MkDocs themes. It maintains a dictionary (`THEMES`) that maps theme names to their corresponding `pip` package names and MkDocs theme names. The `enable_theme` function installs the necessary `pip` package for a given theme, allowing users to easily switch between different visual styles for their documentation.

## `THEMES` Dictionary

This dictionary stores the information about the available themes. Each key represents the theme name, and the corresponding value is another dictionary containing the `package_name` (the name of the `pip` package to install) and `mkdocs_name` (the name used within the `mkdocs.yml` file).

```python
THEMES = {
    "default": {"package_name": "", "mkdocs_name": ""},
    "dracula": {"package_name": "mkdocs-dracula-theme", "mkdocs_name": "dracula"},
    "material": {"package_name": "mkdocs-material", "mkdocs_name": "material"},
}
```

*   `default`: Represents the default MkDocs theme.  `package_name` is empty, so nothing is installed.
*   `dracula`: Specifies the "dracula" theme, which requires the `mkdocs-dracula-theme` `pip` package and uses "dracula" as the theme name in `mkdocs.yml`.
*   `material`: Specifies the "material" theme, which requires the `mkdocs-material` `pip` package and uses "material" as the theme name in `mkdocs.yml`.

## `enable_theme` Function

This function installs the specified MkDocs theme package using `pip`.

```python
def enable_theme(theme="dracula"):
    subprocess.run(
        ["pip", "install", THEMES[theme]["package_name"]],
        check=True,
        capture_output=True,
        text=True,
    )
    pass
```

**Parameters:**

*   `theme` (str, optional): The name of the theme to enable. Defaults to "dracula". It must be a key present in the `THEMES` dictionary.

**Functionality:**

1.  Retrieves the `package_name` from the `THEMES` dictionary using the provided `theme` name.
2.  Executes the `pip install` command using `subprocess.run` to install the specified package.
    *   `check=True`: Raises a `subprocess.CalledProcessError` if the command returns a non-zero exit code, indicating an error during installation.
    *   `capture_output=True`: Captures the standard output and standard error streams of the `pip` command.
    *   `text=True`: Decodes the captured output as text.

**Example Usage:**

```python
import themes

# Enable the Dracula theme
themes.enable_theme("dracula")

# Enable the Material theme
themes.enable_theme("material")
```

**Interaction with other modules:**

This function is called by `mkdocs.update_mkdocs_nav` after the mkdocs configuration file, `mkdocs.yml`, has been updated to use the relevant theme.
It installs the necessary `pip` package to apply the configuration.

## Error Handling

The `enable_theme` function uses `check=True` in `subprocess.run`.  If the `pip install` command fails (e.g., due to network issues or an invalid package name), a `subprocess.CalledProcessError` will be raised, halting the execution. It's good practice to wrap this call in a `try...except` block in the calling function (`mkdocs.update_mkdocs_nav`) to handle potential installation errors gracefully.
