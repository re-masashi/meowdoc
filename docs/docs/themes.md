# `themes.py` Module Documentation

This module defines available MkDocs themes and provides a function to enable a selected theme by installing the necessary `pip` package. It interacts with the operating system by using the `subprocess` module to execute `pip` commands. It is used by `mkdocs.py` to enable the chosen theme.

## Module Contents

### `THEMES`

```python
THEMES = {
    "default": {"package_name": "", "mkdocs_name": ""},
    "dracula": {"package_name": "mkdocs-dracula-theme", "mkdocs_name": "dracula"},
    "material": {"package_name": "mkdocs-material", "mkdocs_name": "material"},
}
```

A dictionary containing information about available MkDocs themes. Each key represents the theme name, and the value is another dictionary containing:

*   `package_name`: The name of the `pip` package to install for the theme (empty string for default).
*   `mkdocs_name`: The name of the theme to use in the `mkdocs.yml` configuration file.

**Example:**

To use the Dracula theme, the `package_name` is `"mkdocs-dracula-theme"` which gets passed to `pip install`. The `mkdocs_name` is `"dracula"` which is used in the `mkdocs.yml` file under the `theme` key.  `mkdocs.py` reads this value and updates `mkdocs.yml`.

### `enable_theme(theme="dracula")`

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

Enables the specified MkDocs theme by installing the corresponding `pip` package.

**Parameters:**

*   `theme` (str, optional): The name of the theme to enable. Must be a key in the `THEMES` dictionary. Defaults to `"dracula"`.

**Raises:**

*   `subprocess.CalledProcessError`: If the `pip install` command fails.

**Example Usage:**

```python
import themes

# Enable the Dracula theme
themes.enable_theme("dracula")

# Enable the Material theme
themes.enable_theme("material")
```

**How it Works:**

1.  The function retrieves the `package_name` associated with the given `theme` from the `THEMES` dictionary.
2.  It uses `subprocess.run` to execute the `pip install` command with the retrieved `package_name`.
    *   `check=True` raises a `CalledProcessError` if the command returns a non-zero exit code (indicating failure).
    *   `capture_output=True` captures the standard output and standard error streams of the subprocess.
    *   `text=True` decodes the captured output as text.
3.  The function then does nothing with the `pass` statement.

**Interaction with Other Modules:**

This function is called by `mkdocs.py` after the `mkdocs.yml` file has been updated with the theme information.  It ensures the necessary theme package is installed.
