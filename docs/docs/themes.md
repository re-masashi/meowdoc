```markdown
# `themes.py` Documentation

This module provides functionality to manage and enable themes for MkDocs documentation projects using `meowdoc`. It defines a dictionary of supported themes and a function to install and activate a specified theme.

## Module Overview

The `themes.py` module is responsible for:

- Defining a dictionary (`THEMES`) that maps theme names to their corresponding package names and MkDocs names.
- Providing a function (`enable_theme`) to install a specified theme using `pip`.

## `THEMES` Dictionary

```python
THEMES = {
    "default": {"package_name": "", "mkdocs_name": ""},
    "dracula": {"package_name": "mkdocs-dracula-theme", "mkdocs_name": "dracula"},
    "material": {"package_name": "mkdocs-material", "mkdocs_name": "material"},
}
```

This dictionary stores information about available themes.  Each key represents a theme name (e.g., "default", "dracula", "material"). The value associated with each theme name is another dictionary containing two keys:

- `"package_name"`: The name of the Python package that provides the theme. This is used with `pip install`.
- `"mkdocs_name"`: The name of the theme as recognized by MkDocs.  This is used when configuring the theme in `mkdocs.yml`.

**Example:**

The "dracula" theme is associated with the package `"mkdocs-dracula-theme"` and the MkDocs name `"dracula"`. This means that to use the Dracula theme, the `mkdocs-dracula-theme` package must be installed, and the `theme` setting in `mkdocs.yml` should be set to `"dracula"`.

The "default" theme has empty strings for both `package_name` and `mkdocs_name`, implying it's the built-in MkDocs theme that doesn't require a separate package.

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

**Parameters:**

- `theme` (str, optional): The name of the theme to enable. Defaults to "dracula". It's a key from `THEMES` dictionary.

**Functionality:**

1.  **Package Name Lookup:**  It retrieves the `package_name` associated with the specified `theme` from the `THEMES` dictionary.
2.  **`pip` Installation:** It uses the `subprocess.run` function to execute the `pip install` command with the retrieved `package_name`.
    -   `check=True`:  Raises a `subprocess.CalledProcessError` if the `pip` command fails (returns a non-zero exit code).
    -   `capture_output=True`: Captures the standard output and standard error streams of the `pip` command.
    -   `text=True`: Decodes the captured output as text.

**Example Usage:**

```python
from meowdoc import themes

themes.enable_theme("material")  # Installs the mkdocs-material theme.
```

**Interactions with other modules:**

This function is called by `mkdocs.py`'s `update_mkdocs_nav` function to ensure the correct theme package is installed after the `mkdocs.yml` file has been updated.

**Error Handling:**

The `check=True` argument in `subprocess.run` will raise an exception if the `pip install` command fails.  The calling code (in `mkdocs.py`) should handle this exception.  The  `capture_output=True` provides additional details in the error message if the install fails.

## Relationship to Other Modules

-   **`mkdocs.py`**: This module uses the `THEMES` dictionary to determine the correct MkDocs theme name and calls the `enable_theme` function to install the theme package.  Specifically, `update_mkdocs_nav` calls `enable_theme`.
-   **`cli.py`**:  Indirectly, `cli.py` uses `themes.py`. It allows specifying the theme as an argument, which is then used when calling `mkdocs.py` to update the MkDocs configuration, which then calls `themes.py`.
-   **`core.py`**: This module is not directly coupled with `themes.py`.
```