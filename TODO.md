## TODO

Legend:
- 🔴 not started
- 🟡 in progress
- 🟢 done

---

### 0) Project setup
- 🔴 Choose a wiki (not wikipedia.org) and verify its license/terms allow scraping
- 🔴 Set base URL and article link prefix (e.g., `/wiki/`)
- 🔴 Create virtual environment and `requirements.txt`
- 🔴 Add `.gitignore` (venv, cache, pycache, etc.)
- 🔴 Initialize git repo and make regular commits

---

### 1) Core architecture (importable modules)
- 🔴 Implement `models.py` (`Page`, traversal `Node/State`)
- 🔴 Implement `cli.py` argument parsing (without `argparse` if required)
- 🔴 Implement `controller.py` (main controller class, receives parsed config)
- 🔴 Implement `scraper.py` (network fetch + optional local HTML mode)
- 🔴 Implement `html_parser.py` (extract content-only text, links, tables)
- 🔴 Implement `cache.py` (disk cache read/write)
- 🔴 Implement `text_utils.py` (tokenize, normalize, count_words, summary)
- 🔴 Implement `output.py` (pretty console/table output)
- 🔴 Create `wiki_scraper.py` entry point (calls CLI + controller)

---

### 2) CLI commands (functional requirements)
- 🔴 `--summary "phrase"`: print first paragraph text (no HTML)
- 🔴 Handle missing article / not found cases gracefully

- 🔴 `--table "phrase" --number n [--first-row-is-header]`
  - 🔴 Extract nth `<table>` and convert to pandas DataFrame
  - 🔴 Save to `"phrase.csv"`
  - 🔴 Print value counts table (excluding headers)

- 🔴 `--count-words "phrase"`
  - 🔴 Extract full article text (no menus/sidebars)
  - 🔴 Update cumulative `./word-counts.json`

- 🔴 `--analyze-relative-word-frequency --mode {article|language} --count n [--chart path]`
  - 🔴 Load top 1000+ language word frequencies (e.g., `wordfreq`)
  - 🔴 Build DataFrame: word, freq_in_article_norm, freq_in_language_norm
  - 🔴 Print DataFrame (pandas-style)
  - 🔴 Optional: save bar chart image with legend and title

- 🔴 `--auto-count-words "start" --depth n --wait t`
  - 🔴 Traverse wiki graph (BFS or DFS)
  - 🔴 Track visited pages
  - 🔴 Respect depth limit and delay between requests
  - 🔴 Reuse `--count-words` logic for each visited page

---

### 3) Testing (offline)
- 🔴 Add `tests/data/` with at least one saved HTML page (e.g., `team_rocket.html`)

- 🔴 Write 4 unit tests (no internet):
  - 🔴 `is_article_link(href)` correctly classifies links
  - 🔴 `phrase_to_url("Team Rocket")` builds correct URL
  - 🔴 `extract_first_paragraph(html)` returns expected start/end
  - 🔴 `count_words("a a b")` returns correct counts

- 🔴 Integration test program:
  - 🔴 Create `tests/wiki_scraper_integration_test.py`
  - 🔴 Ensure it runs via `python wiki_scraper_integration_test.py`
  - 🔴 Load HTML from disk (no network)
  - 🔴 Test one main feature (e.g., summary) using assertions
  - 🔴 Exit with non-zero code on failure

---

### 4) Language detection analysis (Jupyter)
- 🔴 Define `lang_confidence_score(word_counts, language_words_with_frequency)`
- 🔴 Collect language frequency lists (≥ 1000 words) for 3 languages
- 🔴 Prepare test datasets:
  - 🔴 Long wiki article (≥ 5000 words) via `word-counts.json`
  - 🔴 Short wiki article (≥ 20 words) minimizing score for wiki language
  - 🔴 Long non-wiki text for each of the 3 languages

- 🔴 Evaluate for k = 3, 10, 100, 1000 across:
  - 🔴 3 languages × 5 texts

- 🔴 Create clear plots for results
- 🔴 Write conclusions answering:
  - 🔴 Does language choice matter?
  - 🔴 Do frequencies show inflection-rich language behavior?
  - 🔴 Was it hard to find a low-score wiki article and why?

---

### 5) Final polish
- 🔴 Ensure code is PEP8-compliant (≤ 3 intentional deviations allowed)
- 🔴 Ensure modules are importable in REPL/Jupyter
- 🔴 Update README with usage examples for each CLI command
- 🔴 Confirm `cache/` is ignored by git, but `tests/data/` is committed
- 🔴 Dry-run presentation: explain module responsibilities and used libraries
