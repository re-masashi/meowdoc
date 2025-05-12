import os
import logging
import fnmatch
import pathlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil

class MeowdocCore:
    """A class to generate documentation for Python files using LLM and MkDocs."""

    def __init__(
        self, 
        input_path,
        mkdocs_dir,
        docs_dir,
        ignore_patterns,
        project_name,
        project_description,
        repo_url,
        llm_provider,
#         model="gemini-2.0-flash-exp",
    ):
        """Initialize the DocumentationGenerator with a specified AI model."""
        self.input_path=input_path
        self.mkdocs_dir=mkdocs_dir
        self.docs_dir=docs_dir
        self.ignore_patterns=ignore_patterns
        self.project_name=project_name
        self.project_description=project_description
        self.repo_url=repo_url
        self.llm_provider = llm_provider
#        self.model = model
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def generate_docs(self, file_path, all_file_contents):
        """Generates documentation for a single file with context from all related files."""
        filename = os.path.basename(file_path)
        relative_filename = os.path.relpath(file_path, self.input_path) # Get the relative path
        filename = relative_filename

        try:
            code = all_file_contents[filename]
        except KeyError:
            logging.error(f"File content not found for {file_path}")
            return None
        finally:
            logging.info(f"File content found for {file_path}")

        prompt = "Generate comprehensive documentation in Markdown format for the following Python file (do not give the Markdown in backticks.), considering the context of related files:\n\n"
        prompt += f"File: {filename}\n```python\n{code}\n```\n\n"

        prompt += "Context from related files:\n\n"
        for other_filename, other_code in all_file_contents.items():
            if other_filename != filename:
                prompt += f"File: {other_filename}\n```python\n{other_code}\n```\n\n"

        prompt += """
        Include:
        *   A concise Module-level description.
        *   Descriptions of functions and classes, including parameters, return values, and docstrings.
        *   Clearly indicate how this file interacts with other modules (using examples).
        *   Provide example usage.
        *   Descriptions of each function and class, including parameters, return values, and docstrings.
        *   Use clear headings and subheadings (e.g., ##, ###).
        *   Provide example usage where possible.
        *   If there are no docstrings, try to infer the purpose of the code based on its structure and variable names.
        """

        # Read docguide content if it exists
        docguide_path = os.path.join("docguide", file_path + ".md")
        if os.path.exists(docguide_path):
            logging.info(f"Docguide content found for {file_path}")
            with open(docguide_path, "r", encoding="utf-8") as guide_file:
                guide_content = guide_file.read()
                # Append guide content to the prompt
                prompt += f"\n\n### Additional Guidelines:\n{guide_content}\n"

        try:
            # response = genai.GenerativeModel(model_name=self.model).generate_content(
            #     prompt
            # )
            response = self.llm_provider.generate(prompt)
            print(f"generated content for `{filename}`")
            return response
        except Exception as e:
            logging.exception(f"Error calling LLM: {e}")
            return None

    def should_ignore(self, path, ignore_patterns):
        """Checks if a path or any of its parent directories should be ignored."""
        path = os.path.abspath(
            path
        )  # Convert to absolute path for consistent comparison
        while path:
            base_name = os.path.basename(path)
            for pattern in ignore_patterns:
                if fnmatch.fnmatch(base_name, pattern):
                    # logging.info(
                    #     f"Ignoring {path} because it matches pattern: {pattern}"
                    # )
                    return True
            path = os.path.dirname(path)  # Move up to the parent directory
            if path == os.path.dirname(path):  # Check for root
                break
        return False

    def _collect_files(self):
        """Walk input_path and return list of (file_path, relative_path)."""
        file_list = []
        for root, _, files in os.walk(self.input_path):
            if self.should_ignore(root, self.ignore_patterns):
                continue
            for fname in files:
                fp = os.path.join(root, fname)
                if self.should_ignore(fp, self.ignore_patterns):
                    continue
                rel = os.path.relpath(fp, self.input_path)
                file_list.append((fp, rel))
        return file_list

    def process_path(self):
        """Concurrent version of the old process_path; returns list of generated docs."""
        files = self._collect_files()
        all_contents = {}
        # Pre‑read all files into memory (so reading itself can be parallelized too)
        for fp, rel in files:
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    all_contents[rel] = f.read()
            except Exception as e:
                logging.error(f"Failed reading {fp}: {e}")

        mkdocs_docs = os.path.join(self.mkdocs_dir, self.docs_dir)
        pathlib.Path(mkdocs_docs).mkdir(parents=True, exist_ok=True)

        results = []
        # Use ThreadPoolExecutor for I/O-bound work
        with ThreadPoolExecutor() as exe:
            future_to_file = {
                exe.submit(self.generate_docs, fp, all_contents): (fp, rel)
                for fp, rel in files
            }
            for fut in as_completed(future_to_file):
                fp, rel = future_to_file[fut]
                docs = fut.result()
                if docs:
                    out_fname = os.path.splitext(os.path.basename(rel))[0] + '.md'
                    out_path = os.path.join(mkdocs_docs, os.path.dirname(rel), out_fname)
                    pathlib.Path(os.path.dirname(out_path)).mkdir(parents=True, exist_ok=True)
                    with open(out_path, 'w', encoding='utf-8') as out:
                        out.write(docs)
                    results.append(out_path)
                else:
                    logging.error(f"No docs for {fp}")
        return results

    def process_docguide_pages(self):
        """
        Processes files in docguide/pages for inclusion in docs.
        Copies .md files and generates content from .ai.md files using the LLM.
        Returns a list of relative paths from the docs_dir_name for processed pages.
        """
        pages_input_dir = os.path.join("docguide", "(pages)")
        output_docs_dir_full = os.path.join(self.mkdocs_dir, self.docs_dir)
        processed_page_relative_paths = []

        if not os.path.exists(pages_input_dir):
            logging.info(f"Docguide pages directory not found: {pages_input_dir}. Skipping page processing.")
            return processed_page_relative_paths # Return empty list if directory doesn't exist

        logging.info(f"Processing docguide pages from: {pages_input_dir}")

        # Use ThreadPoolExecutor for processing pages (mix of I/O and LLM calls)
        with ThreadPoolExecutor() as page_exe:
             future_to_filepath = {}
             for root, _, files in os.walk(pages_input_dir):
                 # Calculate the corresponding output subdirectory relative to docs_dir_name
                 relative_to_pages_input = os.path.relpath(root, pages_input_dir)

                 for fname in files:
                     input_filepath = os.path.join(root, fname)
                     # Only process .md or .ai.md files
                     if not (fname.endswith(".md") or fname.endswith(".ai.md")):
                         logging.debug(f"Skipping unsupported file in docguide/pages: {input_filepath}")
                         continue

                     output_fname_base, ext = os.path.splitext(fname)
                     # If it's .ai.md, output is .md; if it's .md, output is .md
                     if ext == '.ai': # Handle .ai.md case specifically
                         output_fname = output_fname_base # The base name is already the desired filename
                         output_fname += ".md" # Add the .md extension

                     elif ext == '.md' and not fname.endswith('.ai.md'): # Handle .md files that are not .ai.md
                          output_fname = fname # Keep original filename

                     else:
                          logging.debug(f"Skipping file with unexpected extension in docguide/pages: {input_filepath}")
                          continue

                     # Calculate the full output path within the docs directory
                     output_filepath = os.path.join(output_docs_dir_full, relative_to_pages_input, output_fname)

                     # Calculate the relative path from docs_dir_name for nav
                     relative_output_path_for_nav = os.path.relpath(output_filepath, output_docs_dir_full)

                     # Submit task to executor
                     future_to_filepath[page_exe.submit(
                         self._process_single_docguide_page,
                         input_filepath,
                         output_filepath,
                         relative_output_path_for_nav,
                         fname.endswith(".ai.md") # Flag to indicate if AI generation is needed
                     )] = input_filepath # Store input path for logging errors

             for fut in as_completed(future_to_filepath):
                 input_filepath = future_to_filepath[fut]
                 try:
                      result = fut.result() # result is the relative_output_path_for_nav or None
                      if result:
                           processed_page_relative_paths.append(result)
                 except Exception as e:
                      logging.error(f"Error processing docguide page {input_filepath}: {e}")

        return processed_page_relative_paths

    def _process_single_docguide_page(self, input_filepath, output_filepath, relative_output_path_for_nav, use_ai):
         """Helper function to process a single docguide page file."""
         try:
             # Ensure output directory exists
             pathlib.Path(os.path.dirname(output_filepath)).mkdir(parents=True, exist_ok=True)

             if use_ai:
                 # AI generated Markdown file
                 logging.info(f"Generating docguide page from prompt: {input_filepath}")
                 with open(input_filepath, 'r', encoding='utf-8') as prompt_file:
                     prompt_content = prompt_file.read()

                 generated_content = self.llm_provider.generate(prompt_content)

                 if generated_content:
                     with open(output_filepath, 'w', encoding='utf-8') as outfile:
                         outfile.write(generated_content)
                     logging.info(f"Generated docguide page saved to: {output_filepath}")
                     return relative_output_path_for_nav # Return relative path on success
                 else:
                     logging.warning(f"LLM generated no content for {input_filepath}") # Changed error to warning
                     return None # Return None if generation failed or empty

             else:
                 # Direct Markdown file - Copy
                 logging.info(f"Copying docguide page: {input_filepath} to {output_filepath}")
                 shutil.copyfile(input_filepath, output_filepath)
                 logging.info(f"Copied docguide page saved to: {output_filepath}")
                 return relative_output_path_for_nav # Return relative path on success

         except Exception as e:
             logging.exception(f"Error processing docguide page {input_filepath}: {e}")
             return None # Return None on error

    def create_project_index(
        self,
    ):
        mkdocs_dir=self.mkdocs_dir
        docs_dir=self.docs_dir
        project_name=self.project_name
        project_description=self.project_description

        project_name = project_name.lower().replace("_", "-")

        # Generate AI-based description
        def generate_ai_description(prompt):
            try:
                response = self.llm_provider.generate(prompt)
                print("generated description")
                return response
            except Exception as e:
                logging.error(f"Error calling Gemini API: {e}")
                return "AI-generated content could not be loaded."

        contributing_prompt = f"""
        Generate a 'Contributing' section for a project named {project_name} in markdown. Do not give the response in backticks. 
        Include guidelines for contributing, such as setting up the development environment and submitting pull requests.
        """
        contributing_description = generate_ai_description(contributing_prompt)

        # Create the index content
        index_content = f"""# {project_name}

{project_description}

## Getting Started

This section provides a quick overview of how to get started with {project_name}.

### Installation

```bash
pip install {project_name}
```
Contributing

{contributing_description}
License

MIT License
Repository

GitHub
"""
        # Write the content to index.md
        index_path = os.path.join(mkdocs_dir, docs_dir, "index.md")
        with open(index_path, "w", encoding="utf-8") as outfile:
            outfile.write(index_content)
            print(f"index.md written to: {index_path}")
