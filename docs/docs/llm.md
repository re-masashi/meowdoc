# `llm.py` Documentation

## Module Description

This module defines an abstract base class and concrete classes for interacting with different Large Language Model (LLM) providers such as Google Gemini, OpenAI, and Ollama (a local LLM runner). It also includes a factory function to initialize the appropriate LLM provider based on a configuration dictionary.

This module is a core component of Meowdoc, responsible for interfacing with LLMs to generate documentation from Python code.  It is used by `core.py` to obtain the LLM-generated documentation strings that are then written to Markdown files within the MkDocs documentation structure.

## Classes

### `LLMProvider(ABC)`

#### Description

Abstract base class for all LLM providers.  Defines the interface that concrete LLM provider classes must implement.

#### Methods

*   `generate(prompt: str) -> str`:
    *   **Description:** Abstract method that generates a response based on the provided prompt.
    *   **Parameters:**
        *   `prompt` (`str`): The input prompt for the LLM.
    *   **Returns:**
        *   `str`: The generated response from the LLM.

### `GeminiProvider(LLMProvider)`

#### Description

LLM provider for Google Gemini.  Implements the `LLMProvider` interface to interact with the Gemini API.

#### Attributes

*   `api_key` (`str`): The API key for accessing the Gemini API.
*   `model` (`str`): The name of the Gemini model to use.

#### Methods

*   `__init__(api_key: str, model: str)`:
    *   **Description:** Initializes a new instance of the `GeminiProvider` class.
    *   **Parameters:**
        *   `api_key` (`str`): The API key for accessing the Gemini API.
        *   `model` (`str`): The name of the Gemini model to use.
    *   **Raises:**
        *   `google.generativeai.APIError`: If the API key is invalid or the model is not found.

*   `generate(prompt: str) -> str`:
    *   **Description:** Generates a response from the Gemini API based on the provided prompt.
    *   **Parameters:**
        *   `prompt` (`str`): The input prompt for the Gemini model.
    *   **Returns:**
        *   `str`: The generated response from the Gemini model. Returns an empty string if an error occurs.
    *   **Example:**
        ```python
        from meowdoc import llm
        # Assuming you have initialized the GeminiProvider correctly
        gemini_provider = llm.GeminiProvider(api_key="YOUR_API_KEY", model="gemini-pro")
        prompt = "Write a short poem about cats."
        response = gemini_provider.generate(prompt)
        print(response)
        ```

### `OpenAiProvider(LLMProvider)`

#### Description

LLM provider for OpenAI. Implements the `LLMProvider` interface to interact with the OpenAI API.

#### Attributes

*   `api_key` (`str`): The API key for accessing the OpenAI API.
*   `model` (`str`): The name of the OpenAI model to use.

#### Methods

*   `__init__(api_key: str, model: str)`:
    *   **Description:** Initializes a new instance of the `OpenAiProvider` class.
    *   **Parameters:**
        *   `api_key` (`str`): The API key for accessing the OpenAI API.
        *   `model` (`str`): The name of the OpenAI model to use.

*   `generate(prompt: str) -> str`:
    *   **Description:** Generates a response from the OpenAI API based on the provided prompt.
    *   **Parameters:**
        *   `prompt` (`str`): The input prompt for the OpenAI model.
    *   **Returns:**
        *   `str`: The generated response from the OpenAI model. Returns an empty string if an error occurs.
    *   **Example:**
        ```python
        from meowdoc import llm
        # Assuming you have initialized the OpenAiProvider correctly
        openai_provider = llm.OpenAiProvider(api_key="YOUR_API_KEY", model="text-davinci-003")
        prompt = "Write a short poem about dogs."
        response = openai_provider.generate(prompt)
        print(response)
        ```

### `OllamaProvider(LLMProvider)`

#### Description

LLM provider for Ollama, a local LLM runner. Implements the `LLMProvider` interface to interact with the Ollama API.

#### Attributes

*   `base_url` (`str`): The base URL of the Ollama API.
*   `model` (`str`): The name of the Ollama model to use.

#### Methods

*   `__init__(base_url: str, model: str)`:
    *   **Description:** Initializes a new instance of the `OllamaProvider` class.
    *   **Parameters:**
        *   `base_url` (`str`): The base URL of the Ollama API (e.g., "http://localhost:11434").
        *   `model` (`str`): The name of the Ollama model to use (e.g., "llama2").

*   `generate(prompt: str) -> str`:
    *   **Description:** Generates a response from the Ollama API based on the provided prompt.
    *   **Parameters:**
        *   `prompt` (`str`): The input prompt for the Ollama model.
    *   **Returns:**
        *   `str`: The generated response from the Ollama model. Returns an empty string if an error occurs.
    *   **Example:**
        ```python
        from meowdoc import llm
        # Assuming you have initialized the OllamaProvider correctly
        ollama_provider = llm.OllamaProvider(base_url="http://localhost:11434", model="llama2")
        prompt = "Write a short poem about birds."
        response = ollama_provider.generate(prompt)
        print(response)
        ```

## Functions

### `get_llm_provider(config: dict) -> LLMProvider`

#### Description

Factory function that initializes the appropriate LLM provider based on the configuration dictionary.

#### Parameters

*   `config` (`dict`): A dictionary containing the configuration for the LLM provider.  This dictionary should have an `llm` key containing a dictionary with the following keys:
    *   `provider` (`str`): The name of the LLM provider (e.g., "gemini", "openai", "ollama").
    *   `api_key_file` (`str`, optional): Path to a file containing the API key for Gemini or OpenAI. Required if `provider` is "gemini" or "openai".
    *   `base_url` (`str`, optional): The base URL for Ollama. Required if `provider` is "ollama".
    *   `model` (`str`, optional): The name of the model to use.

#### Returns

*   `LLMProvider`: An instance of the specified LLM provider.

#### Raises

*   `ValueError`: If the configuration is invalid or missing required fields.
*   `FileNotFoundError`: If the API key file does not exist.

#### Example

```python
from meowdoc import llm

config = {
    "llm": {
        "provider": "gemini",
        "api_key_file": "api_key.txt",
        "model": "gemini-pro"
    }
}

try:
    llm_provider = llm.get_llm_provider(config)
    print(f"Successfully initialized provider {llm_provider.__class__.__name__}")
except ValueError as e:
    print(f"Error initializing provider: {e}")
except FileNotFoundError as e:
    print(f"Error initializing provider: {e}")


config_ollama = {
    "llm": {
        "provider": "ollama",
        "base_url": "http://localhost:11434",
        "model": "llama2"
    }
}

try:
    llm_provider = llm.get_llm_provider(config_ollama)
    print(f"Successfully initialized provider {llm_provider.__class__.__name__}")
except ValueError as e:
    print(f"Error initializing provider: {e}")
except FileNotFoundError as e:
    print(f"Error initializing provider: {e}")

```

### `read_api_key(path)`

#### Description

Reads the API key from the given file path.

#### Parameters

*   `path` (`str`): The path to the file containing the API key.

#### Returns

*   `str`: The API key read from the file.

#### Example

```python
from meowdoc import llm
api_key = llm.read_api_key("api_key.txt")
print(f"Api Key: {api_key}")
```

## Interaction with other modules

*   **`core.py`**: This module utilizes the `LLMProvider` interface and the `get_llm_provider` function to generate documentation for Python files. The `MeowdocCore` class in `core.py` receives an `LLMProvider` instance during initialization and uses its `generate` method to produce the documentation content.
*   **`cli.py`**: The command-line interface uses the `llm.get_llm_provider` function to initialize the LLM provider based on the configuration provided by the user (either via a configuration file or command-line arguments). The created `LLMProvider` instance is then passed to the `MeowdocCore` object.
*   **`config.toml`** (example config file): This file specifies the LLM provider to use, API keys, model names, and other relevant settings. The `cli.py` module reads this configuration and passes it to `llm.get_llm_provider` for initialization.

### Example usage within `core.py`:

```python
# Inside MeowdocCore.generate_docs in core.py

def generate_docs(self, file_path, all_file_contents):
    # ... other code ...
    response = self.llm_provider.generate(prompt) # Using the injected llm_provider
    # ... other code ...
```

### Example Configuration (`config.toml`):

```toml
[main]
input_path = "path/to/your/python/code"
mkdocs_dir = "mkdocs"
docs_dir_name = "docs"

[ignore]
patterns = [".venv", "venv"]

[project]
name = "My Project"
description = "A brief description of my project"

[llm]
provider = "gemini" # or "openai" or "ollama"
api_key_file = "api_key.txt"  # Required for Gemini and OpenAI
# base_url = "http://localhost:11434" # Required for Ollama
model = "gemini-pro" # or "gpt-3.5-turbo" or "llama2"

```
