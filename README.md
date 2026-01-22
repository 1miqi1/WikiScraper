# WikiScraper

## Project Description
WikiScraper is a modular Python application for downloading and analyzing
Wikipedia articles. The program starts from a given phrase and traverses
the graph of links between articles up to a specified depth.

The project follows object-oriented programming principles, with a clear
separation of responsibilities and reusable modules. Each module can be
imported and used independently, including in a Python REPL or Jupyter
Notebook environment.

---

## Project Structure and File Descriptions

```text
wikiscraper/
├── wiki_scraper.py
├── requirements.txt
├── README.md
├── word-counts.json
├── analysis.ipynb
│
├── wikiscraper/
│   ├── __init__.py
│   ├── cli.py
│   ├── controller.py
│   ├── scraper.py
│   ├── html_parser.py
│   ├── cache.py
│   ├── models.py
│   ├── text_utils.py
│   ├── output.py
│   └── analyze.py
│
├── cache/
│
├── tests/
│   ├── data/
│   │   └── team_rocket.html
│   ├── test_unit_*.py
│   └── wiki_scraper_integration_test.py
│
└── wiki_scraper_integration_test.py
```

---

### Root directory

* **wiki_scraper.py**
  Main entry point of the application, as required by the assignment.
  Parses command-line arguments, initializes the controller, and starts program execution.
  Contains only high-level orchestration logic (`if __name__ == "__main__":`).

* **requirements.txt**
  Lists all external Python dependencies required to run the project (e.g. `requests`,
  `beautifulsoup4`, `pandas`, `matplotlib`, `wordfreq`).

* **README.md**
  Project documentation describing the purpose of the program, its architecture,
  implemented functionalities, testing approach, and usage instructions.

* **word-counts.json**
  Serialized JSON file storing cumulative word occurrence counts produced by the
  `--count-words` and `--auto-count-words` commands.
  This file may be created or updated at runtime.

* **analysis.ipynb**
  Jupyter Notebook used for language analysis.
  Contains the implementation of the `lang_confidence_score` function, experiments
  with different languages and values of *k*, plots, and written analysis of results.

---

### Application package (`wikiscraper/`)

This directory is a Python package containing all reusable, importable modules
implementing the program logic.

* **`__init__.py`**
  Marks the directory as a Python package and enables importing its modules
  in REPL or Jupyter Notebook.

* **cli.py**
  Implements parsing of command-line arguments (without using `argparse`,
  if required). Converts raw input into structured configuration passed to
  the controller.

* **controller.py**
  Central control module of the application.
  Implements program flow, including graph traversal (BFS or DFS), depth control,
  tracking visited articles, and enforcing delays between requests.

* **scraper.py**
  Responsible for retrieving wiki pages.
  Loads HTML either from the network or from a local file/cache and delegates
  HTML processing to `html_parser.py`. Returns structured `Page` objects.

* **html_parser.py**
  Parses raw HTML content of wiki pages.
  Extracts the main article text, the first paragraph, tables, and links to
  other articles while ignoring static page elements (menus, footers, sidebars).

* **cache.py**
  Implements a simple disk-based caching mechanism for downloaded HTML pages.
  Reduces the number of network requests and improves performance.

* **models.py**
  Defines core data structures used throughout the project, such as:

  * `Page` – representation of a single wiki article,
  * `Node` / `State` – representation of traversal state (article name and depth).

* **text_utils.py**
  Contains pure text-processing utilities, including tokenization, word counting,
  normalization, and summary generation.
  Functions in this module are designed to be easily unit-testable.

* **output.py**
  Handles formatting and displaying results.
  Responsible for printing tables, summaries, and other structured outputs to
  the console.

* **analyze.py**
  Implements logic for `--analyze-relative-word-frequency`.
  Compares word frequencies from collected articles with frequency data of a
  given language and optionally generates visualizations.

---

### Cache directory

* **cache/**
  Directory used to store cached HTML files downloaded from the wiki during
  program execution.
  This directory is typically excluded from version control via `.gitignore`.

---

### Tests

* **tests/**
  Contains all automated tests for the project.

* **tests/data/team_rocket.html**
  Locally stored HTML file used for offline testing and integration tests.
  Allows testing without making network requests.

* **tests/test_unit_*.py**
  Unit tests verifying individual functions or methods (e.g. link detection,
  text processing utilities, HTML parsing helpers).
  Tests do not perform any network communication.

* **tests/wiki_scraper_integration_test.py**
  Integration test executed as a standalone program.
  Loads HTML from disk, runs a selected main functionality (e.g. `--summary`),
  and exits with a non-zero status code if the test fails.

---

### Optional root-level integration test

* **wiki_scraper_integration_test.py**
  Optional copy of the integration test placed in the root directory for
  easier execution using:

  ```bash
  python wiki_scraper_integration_test.py
  ```

## TODO (Development Plan)

See [TODO.md](TODO.md) for the development checklist.

