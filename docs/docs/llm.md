# `llm.py` Documentation

This module defines an abstract base class (`LLMProvider`) and concrete implementations for interacting with different Large Language Models (LLMs) such as Google Gemini, OpenAI, and Ollama (local LLM).  It also provides utility functions for retrieving the appropriate LLM provider based on configuration and reading API keys.

## Table of Contents

1.  [Classes](#classes)
    *   [LLMProvider](#llmprovider)
    *   [GeminiProvider](#geminiprovider)
    *   [OpenAiProvider](#openaiprovider)
    *   [OllamaProvider](#ollamaprovider)
2.  [Functions](#functions)
    *   [get\_llm\_provider](#get_llm_provider)
    *   [read\_api\_key](#read_api_key)

## Classes

<a name="llmprovider"></a>

### `LLMProvider(ABC)`

Bases: `abc.ABC`

Abstract base class for LLM providers. This class defines the interface that all LLM provider implementations must adhere to.

#### Abstract Methods

<a name="llmprovider.generate"></a>

##### `generate(prompt: str) -> str`

Abstract method to generate a response based on a given prompt.  This method must be implemented by all concrete LLM provider classes.

*   **Parameters:**
    *   `prompt` (*str*): The input prompt for the LLM.

*   **Returns:**
    *   *str*: The generated response from the LLM.

<a name="geminiprovider"></a>

### `GeminiProvider(LLMProvider)`

Bases: `llm.LLMProvider`

LLM provider implementation for Google Gemini.  It handles authentication and interaction with the Google Gemini API.

#### Attributes

*   `api_key` (*str*): The API key for accessing the Gemini API.
*   `model` (*str*): The name of the Gemini model to use.

#### Methods

<a name="geminiprovider.__init__"></a>

##### `__init__(api_key: str, model: str)`

Initializes the `GeminiProvider` with an API key and model name.

*   **Parameters:**
    *   `api_key` (*str*): The API key for Google Gemini.
    *   `model` (*str*): The name of the Gemini model to use (e.g., "gemini-1.0-pro").

<a name="geminiprovider.generate"></a>

##### `generate(prompt: str) -> str`

Generates a response from the Google Gemini API based on the provided prompt.

*   **Parameters:**
    *   `prompt` (*str*): The input prompt for Gemini.

*   **Returns:**
    *   *str*: The generated response from Gemini, or an empty string if an error occurs.  Errors are logged using the `logging` module.

*   **Example:**
    ```python
    provider = GeminiProvider(api_key="YOUR_API_KEY", model="gemini-1.0-pro")
    response = provider.generate("Write a short poem about the ocean.")
    print(response)
    ```

<a name="openaiprovider"></a>

### `OpenAiProvider(LLMProvider)`

Bases: `llm.LLMProvider`

LLM provider implementation for OpenAI. It handles authentication and interaction with the OpenAI API.

#### Attributes

*   `api_key` (*str*): The API key for accessing the OpenAI API.
*   `model` (*str*): The name of the OpenAI model to use.

#### Methods

<a name="openaiprovider.__init__"></a>

##### `__init__(api_key: str, model: str)`

Initializes the `OpenAiProvider` with an API key and model name.

*   **Parameters:**
    *   `api_key` (*str*): The API key for OpenAI.
    *   `model` (*str*): The name of the OpenAI model to use (e.g., "text-davinci-003").

<a name="openaiprovider.generate"></a>

##### `generate(prompt: str) -> str`

Generates a response from the OpenAI API based on the provided prompt.

*   **Parameters:**
    *   `prompt` (*str*): The input prompt for OpenAI.

*   **Returns:**
    *   *str*: The generated response from OpenAI, or an empty string if an error occurs. Errors are logged using the `logging` module.

*   **Example:**
    ```python
    provider = OpenAiProvider(api_key="YOUR_API_KEY", model="text-davinci-003")
    response = provider.generate("Translate 'Hello, world!' to French.")
    print(response)
    ```

<a name="ollamaprovider"></a>

### `OllamaProvider(LLMProvider)`

Bases: `llm.LLMProvider`

LLM provider implementation for Ollama, which allows running LLMs locally.

#### Attributes

*   `base_url` (*str*): The base URL of the Ollama API.
*   `model` (*str*): The name of the Ollama model to use.

#### Methods

<a name="ollamaprovider.__init__"></a>

##### `__init__(base_url: str, model: str)`

Initializes the `OllamaProvider` with the base URL and model name.

*   **Parameters:**
    *   `base_url` (*str*): The base URL of the Ollama API (e.g., "http://localhost:11434").
    *   `model` (*str*): The name of the Ollama model to use (e.g., "llama2").

<a name="ollamaprovider.generate"></a>

##### `generate(prompt: str) -> str`

Generates a response from the local Ollama API based on the provided prompt.

*   **Parameters:**
    *   `prompt` (*str*): The input prompt for Ollama.

*   **Returns:**
    *   *str*: The generated response from Ollama, or an empty string if an error occurs. Errors are logged using the `logging` module.

*   **Example:**
    ```python
    provider = OllamaProvider(base_url="http://localhost:11434", model="llama2")
    response = provider.generate("Explain the concept of recursion.")
    print(response)
    ```

## Functions

<a name="get_llm_provider"></a>

### `get_llm_provider(config: dict) -> LLMProvider`

Initializes and returns an LLM provider based on the configuration.

*   **Parameters:**
    *   `config` (*dict*): A dictionary containing the LLM settings.  The dictionary should have the following structure:

        ```python
        {
            "llm": {
                "provider": "gemini" | "openai" | "ollama",
                "api_key_file": "path/to/api_key.txt",  # Required for Gemini and OpenAI
                "base_url": "http://localhost:11434",   # Required for Ollama
                "model": "model_name"
            }
        }
        ```

*   **Returns:**
    *   `LLMProvider`: An instance of the specified LLM provider (`GeminiProvider`, `OpenAiProvider`, or `OllamaProvider`).

*   **Raises:**
    *   `ValueError`: If the configuration is invalid, missing required fields, or an unsupported LLM provider is specified.

*   **Example:**
    ```python
    config = {
        "llm": {
            "provider": "gemini",
            "api_key_file": "api_key.txt",
            "model": "gemini-1.0-pro"
        }
    }
    provider = get_llm_provider(config)
    ```

<a name="read_api_key"></a>

### `read_api_key(path: str) -> str`

Reads an API key from a file.

*   **Parameters:**
    *   `path` (*str*): The path to the file containing the API key.

*   **Returns:**
    *   *str*: The API key read from the file.

*   **Example:**
    ```python
    api_key = read_api_key("api_key.txt")
    ```

## Usage in Context

This `llm.py` module is used by `core.py` to generate documentation. The `MeowdocCore` class in `core.py` takes an `LLMProvider` instance as input and uses it to generate documentation for Python files. The `cli.py` script uses the `get_llm_provider` function to initialize the LLM provider based on the configuration provided by the user via command-line arguments or a configuration file.
`mkdocs.py` is then used to format the files in the correct Markdown format.
