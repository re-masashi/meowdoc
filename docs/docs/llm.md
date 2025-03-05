# `llm.py` Module Documentation

## Module Description

This module defines an abstract base class (`LLMProvider`) and concrete classes for interacting with different Large Language Model (LLM) providers such as Google Gemini, OpenAI, and Ollama (for local LLMs). It also includes utility functions for initializing an LLM provider based on a configuration dictionary. The module utilizes the `abc`, `google.generativeai`, `openai`, `requests`, and `logging` libraries.

## Classes

### `LLMProvider` (Abstract Base Class)

```python
class LLMProvider(ABC):
```

Base class for all LLM provider implementations.  It defines the abstract method `generate`.

#### Methods

*   `generate(prompt: str) -> str` (Abstract)

    Abstract method that must be implemented by subclasses to generate a text response from the given prompt using the LLM provider.

    *   **Parameters:**
        *   `prompt` (str): The input text prompt for the LLM.
    *   **Returns:**
        *   str: The generated text response from the LLM.

### `GeminiProvider`

```python
class GeminiProvider(LLMProvider):
```

Implementation of `LLMProvider` for interacting with the Google Gemini LLM.

#### Attributes

*   `api_key` (str): The API key for accessing the Google Gemini API.
*   `model` (str): The name of the Gemini model to use.

#### Methods

*   `__init__(api_key: str, model: str)`

    Initializes a new `GeminiProvider` instance.

    *   **Parameters:**
        *   `api_key` (str): The API key for the Google Gemini API.
        *   `model` (str): The name of the Gemini model to use.

*   `generate(prompt: str) -> str`

    Generates a text response from the given prompt using the Google Gemini LLM.

    *   **Parameters:**
        *   `prompt` (str): The input text prompt.
    *   **Returns:**
        *   str: The generated text response from Gemini. Returns an empty string if an error occurs.

    *   **Example Usage:**

        ```python
        from llm import GeminiProvider
        #Assuming you have a valid API key and model name
        api_key = "YOUR_GEMINI_API_KEY"
        model = "gemini-1.5-pro-latest"
        provider = GeminiProvider(api_key, model)
        prompt = "What is the capital of France?"
        response = provider.generate(prompt)
        print(response)
        ```

### `OpenAiProvider`

```python
class OpenAiProvider(LLMProvider):
```

Implementation of `LLMProvider` for interacting with the OpenAI LLM.

#### Attributes

*   `api_key` (str): The API key for accessing the OpenAI API.
*   `model` (str): The name of the OpenAI model to use.

#### Methods

*   `__init__(api_key: str, model: str)`

    Initializes a new `OpenAiProvider` instance.

    *   **Parameters:**
        *   `api_key` (str): The API key for the OpenAI API.
        *   `model` (str): The name of the OpenAI model to use (e.g., "text-davinci-003").

*   `generate(prompt: str) -> str`

    Generates a text response from the given prompt using the OpenAI LLM.

    *   **Parameters:**
        *   `prompt` (str): The input text prompt.
    *   **Returns:**
        *   str: The generated text response from OpenAI. Returns an empty string if an error occurs.

    *   **Example Usage:**

        ```python
        from llm import OpenAiProvider
        #Assuming you have a valid API key and model name
        api_key = "YOUR_OPENAI_API_KEY"
        model = "text-davinci-003"
        provider = OpenAiProvider(api_key, model)
        prompt = "What is the capital of Spain?"
        response = provider.generate(prompt)
        print(response)
        ```

### `OllamaProvider`

```python
class OllamaProvider(LLMProvider):
```

Implementation of `LLMProvider` for interacting with a local LLM served by Ollama.

#### Attributes

*   `base_url` (str): The base URL of the Ollama API endpoint (e.g., "http://localhost:11434").
*   `model` (str): The name of the Ollama model to use.

#### Methods

*   `__init__(base_url: str, model: str)`

    Initializes a new `OllamaProvider` instance.

    *   **Parameters:**
        *   `base_url` (str): The base URL of the Ollama API endpoint.
        *   `model` (str): The name of the Ollama model to use.

*   `generate(prompt: str) -> str`

    Generates a text response from the given prompt using the Ollama LLM.

    *   **Parameters:**
        *   `prompt` (str): The input text prompt.
    *   **Returns:**
        *   str: The generated text response from Ollama. Returns an empty string if an error occurs.

    *   **Example Usage:**

        ```python
        from llm import OllamaProvider
        #Assuming you have Ollama running with a model
        base_url = "http://localhost:11434"
        model = "mistral"
        provider = OllamaProvider(base_url, model)
        prompt = "What is 1 + 1?"
        response = provider.generate(prompt)
        print(response)
        ```

## Functions

### `get_llm_provider(config: dict) -> LLMProvider`

```python
def get_llm_provider(config: dict) -> LLMProvider:
```

Initializes and returns an `LLMProvider` instance based on the provided configuration dictionary.

*   **Parameters:**
    *   `config` (dict): A dictionary containing the LLM provider settings. It should include a `"llm"` section with the following keys:
        *   `"provider"` (str): The name of the LLM provider ("gemini", "openai", or "ollama").
        *   `"api_key_file"` (str, optional): Path to the file containing the API key (required for Gemini and OpenAI).
        *   `"base_url"` (str, optional): The base URL for Ollama (required for Ollama).
        *   `"model"` (str): The name of the LLM model to use.

*   **Returns:**
    *   `LLMProvider`: An instance of the specified LLM provider (either `GeminiProvider`, `OpenAiProvider`, or `OllamaProvider`).

*   **Raises:**
    *   `ValueError`: If the configuration is invalid or missing required fields.

*   **Example Usage:**

    ```python
    from llm import get_llm_provider

    config = {
        "llm": {
            "provider": "gemini",
            "api_key_file": "path/to/your/gemini_api_key.txt",
            "model": "gemini-1.5-pro-latest"
        }
    }
    provider = get_llm_provider(config)
    ```

    ```python
    from llm import get_llm_provider

    config = {
        "llm": {
            "provider": "ollama",
            "base_url": "http://localhost:11434",
            "model": "mistral"
        }
    }
    provider = get_llm_provider(config)
    ```

### `read_api_key(path)`

```python
def read_api_key(path):
```

Reads and returns the API key from the specified file.

*   **Parameters:**

    *   `path` (str): The path to the file containing the API key.

*   **Returns:**

    *   `str`: The API key read from the file.

## Interactions with other modules

*   **`core.py`:** The `get_llm_provider` function is used in `core.py` to initialize the LLM provider that the `MeowdocCore` class uses to generate documentation.  The `MeowdocCore.generate_docs` method calls the `generate` method of the `LLMProvider` instance to get the documentation from the language model. Example:

    ```python
    # From core.py
    class MeowdocCore:
        def __init__(self, ..., llm_provider):
            self.llm_provider = llm_provider

        def generate_docs(self, file_path, all_file_contents):
            ...
            response = self.llm_provider.generate(prompt)
            ...
    ```

*   **`cli.py`:** This module uses `get_llm_provider` function to fetch the LLM Provider instance.
    ```python
    #From cli.py
    def main():
        ...
        llm_provider = get_llm_provider(config)  # Get LLM provider
        ...
    ```

## Error Handling

The module uses `logging` to report errors encountered during API calls. Each provider's `generate` method includes a `try...except` block to catch potential exceptions during the API call. If an error occurs, a message is logged, and an empty string is returned. The `get_llm_provider` function raises a `ValueError` if the configuration is invalid or missing required fields.

## Notes

*   This module requires the `google-generativeai`, `openai`, and `requests` packages to be installed.
*   To use the Gemini and OpenAI providers, you must have a valid API key and set it in the `api_key` attribute.
*   To use the Ollama provider, you must have Ollama installed and running, and set the correct `base_url` and `model` attributes.  Also, ensure you have the model downloaded in Ollama before running this tool.
