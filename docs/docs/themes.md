# `themes.py` Documentation

This module provides functionality for managing and enabling MkDocs themes. It defines a dictionary of available themes and a function to install them using `pip`.

## Module Overview

The module focuses on simplifying the process of switching between different MkDocs themes by providing a central location to define themes and install them. It leverages the `subprocess` module to execute `pip` commands, automating the theme installation process.

## `THEMES` Dictionary

```python
THEMES = {
    "default": {"package_name": "", "mkdocs_name": ""},
    "dracula": {"package_name": "mkdocs-dracula-theme", "mkdocs_name": "dracula"},
    "material": {"package_name": "mkdocs-material", "mkdocs_name": "material"},
}
```

This dictionary stores information about available MkDocs themes. Each key represents a theme name, and the corresponding value is another dictionary containing:

*   `package_name`: The name of the Python package to install using `pip`.  This is the package that provides the MkDocs theme.
*   `mkdocs_name`: The name of the theme as it should be specified in the `mkdocs.yml` configuration file.

Currently, the dictionary includes the "default", "dracula", and "material" themes.  The "default" theme has empty strings for both `package_name` and `mkdocs_name`, implying it relies on default mkdocs configurations.  "dracula" specifies the "mkdocs-dracula-theme" package and the theme name "dracula". "material" specifies the "mkdocs-material" package and the theme name "material".

## `enable_theme(theme="dracula")` Function

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

This function installs the specified MkDocs theme using `pip`.

*   **Parameters:**
    *   `theme` (str, optional): The name of the theme to enable.  It must be a key in the `THEMES` dictionary. Defaults to "dracula".

*   **Functionality:**
    1.  It retrieves the `package_name` associated with the given `theme` from the `THEMES` dictionary.
    2.  It uses `subprocess.run` to execute the `pip install` command.
        *   `check=True`: Raises a `subprocess.CalledProcessError` if the command returns a non-zero exit code, indicating an error during installation.
        *   `capture_output=True`: Captures the standard output and standard error streams of the subprocess, making them available for logging or debugging.
        *   `text=True`: Opens the captured streams in text mode with universal newlines.

*   **Error Handling:**
    *   If the specified `theme` is not found in the `THEMES` dictionary, a `KeyError` will be raised.  This exception is not explicitly handled within the function.
    *   If the `pip install` command fails (e.g., due to network issues or an invalid package name), `subprocess.check_call` will raise a `subprocess.CalledProcessError`. This exception is not explicitly handled within the function.

*   **Example Usage:**

    ```python
    from meowdoc import themes

    themes.enable_theme("material")  # Install the Material theme
    ```

## Integration with Other Modules

This module is primarily used by `mkdocs.py` to install the chosen theme when updating the `mkdocs.yml` configuration file.  The `update_mkdocs_nav` function in `mkdocs.py` calls `themes.enable_theme()` at the end of its process to ensure that the theme is installed before the MkDocs site is built.  This is crucial for the generated documentation to be displayed correctly with the selected theme.

The `cli.py` doesn't directly call this, but indirectly depends on it through the calls to `mkdocs.py`.

## Potential Improvements

*   **Error Handling:**  Add more robust error handling to catch potential exceptions, such as `KeyError` (if the theme doesn't exist) and `subprocess.CalledProcessError` (if the `pip install` command fails).  Log these errors appropriately.
*   **Theme Validation:** Implement a mechanism to validate that the installed theme is actually a valid MkDocs theme.
*   **Dependency Management:**  Consider using a more sophisticated dependency management tool (e.g., `poetry` or `pipenv`) to handle theme installation and versioning.
*   **User Feedback:**  Provide more informative feedback to the user during the theme installation process, such as displaying the output of the `pip install` command.
*   **Theme Configuration:** Allow users to configure theme-specific options (e.g., color schemes) directly within the `themes.py` module or through a configuration file.
*   **Uninstall theme functionality:** add a `disable_theme` function

## Example Usage
```python
from meowdoc import themes

# Enable the Dracula theme (default)
themes.enable_theme()

# Enable the Material theme
themes.enable_theme("material")
```
