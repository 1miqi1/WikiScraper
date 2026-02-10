# WikiScraper

## Project Description
## Project Description

WikiScraper is a modular Python application for downloading and analyzing
articles from a selected wiki. In this project, **Bulbapedia** is used as
the data source, as its license allows non-commercial reuse and it does not
restrict automated data collection.


The project follows object-oriented programming principles, with a clear
separation of responsibilities and reusable modules. Each module can be
imported and used independently, including in a Python REPL or Jupyter
Notebook env


---

## Wiki Configuration

The program is configured to operate on the
[Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Main_Page) wiki.

Article URLs on Bulbapedia follow a consistent structure consisting of a fixed
base URL and an article-specific suffix, where spaces in article titles are
replaced with underscores:

- **Base URL:** `https://bulbapedia.bulbagarden.net/wiki/`
- **Article URL format:**  
  `https://bulbapedia.bulbagarden.net/wiki/<Article_Title>`

For example, the article titled *Team Rocket* is available at:


## Project Structure and File Descriptions

```text
wikiscraper/
├── wiki_scraper.py
├── requirements.txt
├── README.md
├── analysis.ipynb
├── setup.py
│
├── wikiscraper/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── controller.py
│   ├── scraper.py
│   ├── html_parser.py
│   ├── page.py
│
├── data/
│   ├── cache/
│   ├── word-counts.json
│
├── tests/
│   ├── data/
│   ├── test_unit_*.py
│   └── wiki_scraper_integration_test.py
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


* **analysis.ipynb**
  Jupyter Notebook used for language analysis.
  Contains the implementation of the `lang_confidence_score` function, experiments
  with different languages and values of *k*, plots, and written analysis of results.

* **setup.py**
  Packaging and installation configuration for the project.
  Allows installing the project in editable mode (`pip install -e .`) so the `wikiscraper` package can be imported from anywhere within the active virtual environment.



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

* **config.py**  
  Centralizes wiki settings, filesystem paths, and runtime configuration values
  used throughout the application.

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

* **page.py**
  Defines core data structures used throughout the project, such as:

  * `Page` – representation of a single wiki article, with functionalities.


---

### Data directory

* **cache/**
  Directory used to store cached HTML files downloaded from the wiki during
  program execution.
  This directory is typically excluded from version control via `.gitignore`.

* **word-counts.json**
  Serialized JSON file storing cumulative word occurrence counts produced by the
  `--count-words` and `--auto-count-words` commands.
  This file may be created or updated at runtime.

---

### Tests

* **tests/**
  Contains all automated tests for the project.

* **tests/data/**
  Locally stored HTML files used for offline testing and integration tests.
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
Here’s a clean “How to run” section you can paste into your **README.md**. It matches your file layout (`wiki_scraper.py`, venv, integration test) and the assignment’s required commands.


## How to Run

### 1) Set up the environment
Create and activate a virtual environment, then install dependencies:

**Linux / macOS**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
````

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

---



### 2) Run the program

The main entry point is:

```bash
python wiki_scraper.py <arguments>
```

Supported commands (examples):

#### Summary of the first paragraph

```bash
python wiki_scraper.py --summary "Team Rocket"
```

#### Extract a table to CSV

```bash
python wiki_scraper.py --table "Type" --number 2
```

With header in the first row:

```bash
python wiki_scraper.py --table "Type" --number 2 --first-row-is-header
```

#### Count words in an article (updates `./word-counts.json`)

```bash
python wiki_scraper.py --count-words "Team Rocket"
```

#### Compare article word frequency vs. language frequency

```bash
python wiki_scraper.py --analyze-relative-word-frequency --mode "article" --count 20
```

With chart output:

```bash
python wiki_scraper.py --analyze-relative-word-frequency --mode "language" --count 20 --chart "chart.png"
```

#### Automatically count words across linked pages

```bash
python wiki_scraper.py --auto-count-words "Team Rocket" --depth 2 --wait 1
```

---

### 3) Run the integration test

The integration test is a standalone program that loads a saved HTML file from disk
(no network connection) and verifies one core functionality.

Run:

```bash
python wiki_scraper_integration_test.py
```

The test exits with a non-zero status code if it fails.


