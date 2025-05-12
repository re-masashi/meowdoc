```markdown
# `llm.py` Documentation

This module defines an abstract base class for LLM providers and concrete implementations for Google Gemini, OpenAI, and Ollama. It also provides a function to initialize an LLM provider based on a configuration dictionary.

## Table of Contents

1.  [Introduction](#introduction)
2.  [Classes](#classes)
    *   [LLMProvider (Abstract Base Class)](#llmprovider-abstract-base-class)
    *   [GeminiProvider](#geminiprovider)
    *   [OpenAiProvider](#opaiprovider)
    *   [OllamaProvider](#ollamaprovider)
3.  [Functions](#functions)
    *   [get\_llm\_provider](#get_llm_provider)
    *   [read\_api\_key](#read_api_key)
4.  [Usage Examples](#usage-examples)
5.  [Related Files](#related-files)

## Introduction

The `llm.py` module provides a flexible way to integrate different Large Language Models (LLMs) into the MeowDoc documentation generation process. It uses an abstract base class (`LLMProvider`) to define a common interface for all LLM providers, allowing for easy switching between different LLMs without modifying the core application logic.  The module supports Gemini, OpenAI, and local Ollama models.

## Classes

### `LLMProvider` (Abstract Base Class)

```python
class LLMProvider(ABC):
    """Base class for LLM providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response based on the prompt."""
        pass
```

This abstract base class defines the interface for all LLM providers.

*   **`generate(prompt: str) -> str` (Abstract Method):**  This method takes a prompt string as input and returns a string containing the LLM's generated response.  It must be implemented by all concrete subclasses.

### `GeminiProvider`

```python
class GeminiProvider(LLMProvider):
    """LLM provider for Google Gemini."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        genai.configure(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        try:
            response = genai.GenerativeModel(model_name=self.model).generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Error calling Gemini API: {e}")
            return ""
```

This class implements the `LLMProvider` interface for Google's Gemini LLM.

*   **`__init__(self, api_key: str, model: str)`:**
    *   Initializes the `GeminiProvider` with the API key and the model name.
    *   Configures the `google.generativeai` library with the provided API key.
    *   `api_key`: The API key for accessing the Gemini API.  It is read from the path specified by `api_key_file` in the configuration.
    *   `model`: The name of the Gemini model to use (e.g., "gemini-pro").

*   **`generate(self, prompt: str) -> str`:**
    *   Generates a response from the Gemini LLM based on the provided prompt.
    *   Uses `genai.GenerativeModel` to interact with the Gemini API.
    *   Returns the generated text or an empty string if an error occurs.
    *   Handles exceptions and logs errors using the `logging` module.

### `OpenAiProvider`

```python
class OpenAiProvider(LLMProvider):
    """LLM provider for OpenAI."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key

    def generate(self, prompt: str) -> str:
        try:
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                max_tokens=500
            )
            return response.choices[0].text.strip()
        except Exception as e:
            logging.error(f"Error calling OpenAI API: {e}")
            return ""
```

This class implements the `LLMProvider` interface for OpenAI LLMs.

*   **`__init__(self, api_key: str, model: str)`:**
    *   Initializes the `OpenAiProvider` with the API key and the model name.
    *   Sets the `openai.api_key` to the provided API key.
    *   `api_key`: The API key for accessing the OpenAI API. It is read from the path specified by `api_key_file` in the configuration.
    *   `model`: The name of the OpenAI model to use (e.g., "text-davinci-003").

*   **`generate(self, prompt: str) -> str`:**
    *   Generates a response from the OpenAI LLM based on the provided prompt.
    *   Uses `openai.Completion.create` to interact with the OpenAI API.
    *   Returns the generated text, stripped of leading/trailing whitespace, or an empty string if an error occurs.
    *   Sets `max_tokens` to 500 to limit the length of the generated response.
    *   Handles exceptions and logs errors using the `logging` module.

### `OllamaProvider`

```python
class OllamaProvider(LLMProvider):
    """LLM provider for Ollama (local LLM)."""

    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_ctx": 4096
                    }
                }
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            logging.error(f"Error calling Ollama API: {e}")
            return ""
```

This class implements the `LLMProvider` interface for local LLMs served by Ollama.

*   **`__init__(self, base_url: str, model: str)`:**
    *   Initializes the `OllamaProvider` with the base URL of the Ollama server and the model name.
    *   `base_url`: The base URL of the Ollama API (e.g., "http://localhost:11434").
    *   `model`: The name of the Ollama model to use (e.g., "llama2").

*   **`generate(self, prompt: str) -> str`:**
    *   Generates a response from the local Ollama LLM based on the provided prompt.
    *   Uses `requests.post` to send a POST request to the Ollama API's `/api/generate` endpoint.
    *   Sets the `stream` parameter to `False` to receive the entire response at once.
    *   Sets the `num_ctx` option to 4096 to allow for longer context windows.
    *   Returns the generated text from the `"response"` field of the JSON response or an empty string if an error occurs.
    *   Handles exceptions and logs errors using the `logging` module.
    *   Raises an HTTPError if the request fails (e.g., due to server error or invalid URL).

## Functions

### `get_llm_provider`

```python
def get_llm_provider(config: dict) -> LLMProvider:
    """Initialize the LLM provider based on the configuration.

    Args:
        config (dict): Configuration dictionary containing LLM settings.

    Returns:
        LLMProvider: An instance of the specified LLM provider.

    Raises:
        ValueError: If the configuration is invalid or missing required fields.
    """
    provider = config["llm"]["provider"]
    api_key_file = config["llm"].get("api_key_file")
    base_url = config["llm"].get("base_url")
    model = config["llm"].get("model")

    if provider == "gemini":
        if not api_key_file:
            raise ValueError("API key file path is required for Gemini.")
        api_key = read_api_key(api_key_file)
        return GeminiProvider(api_key=api_key, model=model)
    elif provider == "openai":
        if not api_key_file:
            raise ValueError("API key file path is required for OpenAI.")
        api_key = read_api_key(api_key_file)
        return OpenAiProvider(api_key=api_key, model=model)
    elif provider == "ollama":
        if not base_url:
            raise ValueError("Base URL is required for Ollama.")
        return OllamaProvider(base_url=base_url, model=model)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
```

This function initializes an LLM provider based on the provided configuration dictionary.

*   **`config` (dict):** A dictionary containing the configuration for the LLM provider.  The dictionary should have an `llm` key with nested keys for `provider`, `api_key_file` (for Gemini and OpenAI), `base_url` (for Ollama), and `model`.
*   **Returns:** An instance of the specified `LLMProvider` subclass (e.g., `GeminiProvider`, `OpenAiProvider`, or `OllamaProvider`).
*   **Raises:** `ValueError` if the configuration is invalid (e.g., missing required fields, unsupported provider).

The function reads the provider type, API key file path, base URL, and model name from the configuration dictionary.  It then instantiates the appropriate `LLMProvider` subclass based on the provider type.  The API key is read from the file specified by `api_key_file` using the `read_api_key` function.

### `read_api_key`

```python
def read_api_key(path):
    content = ""
    with open(path) as f:
        content = f.read()
    return content
```

This function reads an API key from a file.

*   **`path` (str):** The path to the file containing the API key.
*   **Returns:** The API key as a string.

## Usage Examples

Here's an example of how to use the `get_llm_provider` function:

```python
from llm import get_llm_provider

config = {
    "llm": {
        "provider": "gemini",
        "api_key_file": "api_key.txt",
        "model": "gemini-pro"
    }
}

llm_provider = get_llm_provider(config)

if llm_provider:
    response = llm_provider.generate("Write a short poem about cats.")
    print(response)
```

This example assumes that you have a file named `api_key.txt` containing your Gemini API key.

Another Example, with Ollama:

```python
from llm import get_llm_provider

config = {
    "llm": {
        "provider": "ollama",
        "base_url": "http://localhost:11434",
        "model": "llama2"
    }
}

llm_provider = get_llm_provider(config)

if llm_provider:
    response = llm_provider.generate("Write a short poem about cats.")
    print(response)
```

## Related Files

*   **`__init__.py`:**  This file is an empty initialization file for the `meowdoc` package.
*   **`cli.py`:**  This file contains the command-line interface for MeowDoc. It uses the `llm.py` module to obtain an LLM provider and generate documentation.  The `cli.py` file loads the configuration from a TOML file or command-line arguments and passes it to the `get_llm_provider` function.
*   **`core.py`:** This file contains the core logic for generating documentation. The `MeowdocCore` class uses the `LLMProvider` obtained from `llm.py` to generate documentation for Python files.
*   **`mkdocs.py`:** This file handles the integration with MkDocs, a static site generator.
*   **`themes.py`:** This file manages the installation and selection of MkDocs themes.
*   **`dummy_files/hw.rs`**: A dummy file used for testing purposes.

The `cli.py` script loads the configuration and uses `llm.get_llm_provider` to instantiate the appropriate LLM provider. The `MeowdocCore` class in `core.py` then uses this LLM provider to generate documentation from the provided input files. The generated documentation is then used to update the MkDocs project, updating the navigation and configuration as necessary.
