# Enterprise UI Automation Framework – Books to Scrape

A production-ready UI test automation framework built with **Playwright** and **Pytest**, targeting [books.toscrape.com](https://books.toscrape.com/index.html). The framework follows OOP, SOLID, and DRY principles with a clean Page Object Model architecture.

---

## Project Overview

This framework validates five key quality areas of the Books to Scrape website:
- Homepage content and structure
- Random book navigation correctness
- Data consistency between listing and detail pages
- Broken link detection
- Product image attribute completeness across paginated pages

---

## Features

- ✅ Page Object Model (POM) architecture
- ✅ Pytest fixtures for clean test setup and teardown
- ✅ Randomised book selection (5 books per test run)
- ✅ HTTP link validation via `requests`
- ✅ Multi-page image validation with pagination support
- ✅ HTML report via `pytest-html`
- ✅ Allure report via `allure-pytest`
- ✅ GitHub Actions CI/CD pipeline with artifact upload
- ✅ No hardcoded waits — all synchronisation via Playwright's built-in strategies

---

## Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.8+ | Core language |
| Playwright | 1.50.x | Browser automation |
| pytest-playwright | 0.6.x | Playwright–Pytest integration |
| pytest | 8.x | Test runner |
| pytest-html | 4.x | HTML report generation |
| allure-pytest | 2.x | Allure report generation |
| requests | 2.x | HTTP link validation |

---

## Installation Guide

### Prerequisites

- Python 3.8 or higher
- pip

### 1. Clone the repository

```bash
git clone https://github.com/robiulislam99/Books-Automation_Md_Robiul_Islam.git books-automation
cd books-automation
```

### 2. Create and activate a virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install chromium
```

---

## Environment Setup

No environment variables are required. The base URL is defined in `pages/base_page.py` as a class constant and can be changed there if needed.

---

## Running Tests

### Run the full suite (default: Chromium, headless)

```bash
pytest
```

### Run with a visible browser window

```bash
pytest --headed
```

### Run a single test file

```bash
pytest tests/test_homepage.py -v
```

### Run with a specific browser

```bash
pytest --browser firefox
pytest --browser webkit
```

### Run and keep reports even on failure

```bash
pytest --html=reports/html/report.html --self-contained-html --alluredir=allure-results
```

---

## Project Structure

```
books_automation/
├── .github/
│   └── workflows/
│       └── playwright.yml        # CI/CD pipeline definition
├── pages/
│   ├── __init__.py
│   ├── base_page.py              # Shared browser interaction methods
│   ├── home_page.py              # POM for the homepage / catalogue
│   └── book_detail_page.py      # POM for individual book pages
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Shared fixtures
│   ├── test_homepage.py          # TC-01: Homepage validation
│   ├── test_book_navigation.py   # TC-02: Random book navigation
│   ├── test_data_consistency.py  # TC-03: Data consistency
│   ├── test_broken_links.py      # TC-04: Broken link detection
│   └── test_images.py            # TC-05: Image attribute validation
├── utils/
│   ├── __init__.py
│   └── helpers.py                # HTTP utility functions
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## Test Case Coverage

| ID | Test File | Description |
|---|---|---|
| TC-01 | `test_homepage.py` | Homepage URL, title, headings, book section |
| TC-02 | `test_book_navigation.py` | Random 5 books → detail page H1 + info table |
| TC-03 | `test_data_consistency.py` | Title & price match homepage ↔ detail page |
| TC-04 | `test_broken_links.py` | All anchor hrefs return HTTP 200 |
| TC-05 | `test_images.py` | Image src, alt, class=thumbnail across 5 pages |

---

## Report Generation Guide

### HTML Report

Generated automatically on every test run. Open it in any browser:

```bash
pytest
```

```bash
# macOS
open reports/html/report.html

# Linux
xdg-open reports/html/report.html

# Windows
start reports/html/report.html

# Or paste this path directly into your browser
# file:///path/to/books_automation/reports/html/report.html
```

---

### Allure Report

Allure CLI requires **Java 17+** to run. Follow the steps below based on your environment.

---

#### Option A — Linux with sudo access (no brew/scoop)

```bash
# Step 1: Install Java
sudo apt update
sudo apt install -y default-jre

# Verify Java
java -version

# Step 2: Install Allure via curl
curl -o allure-2.27.0.tgz -L \
  https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz
sudo tar -xzf allure-2.27.0.tgz -C /opt/
sudo ln -s /opt/allure-2.27.0/bin/allure /usr/local/bin/allure

# Verify
allure --version

# Step 3: Run tests and serve report
pytest --alluredir=allure-results
allure serve allure-results
```

---

#### Option B — Java already installed (or installed via package manager)

```bash
# Verify Java
java -version

# Install Allure CLI
# macOS
brew install allure

# Windows (Scoop)
scoop install allure

# Linux (if you have sudo)
sudo apt install allure
```

Then serve the report:

```bash
allure serve allure-results
```

---



#### Option C — No Java, no sudo (Linux)

Download Java and Allure manually without admin rights.

**Step 1: Download Java 17**

```bash
wget --no-check-certificate \
  https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.11%2B9/OpenJDK17U-jdk_x64_linux_hotspot_17.0.11_9.tar.gz

tar -xzf OpenJDK17U-jdk_x64_linux_hotspot_17.0.11_9.tar.gz -C ~/
```

**Step 2: Download Allure 2.27.0**

```bash
python3 -c "
import urllib.request, ssl, os
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url = 'https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.zip'
dest = os.path.expanduser('~/allure.zip')
print('Downloading Allure...')
urllib.request.urlretrieve(url, dest)
print('Done!')
"

python3 -c "
import zipfile, os
with zipfile.ZipFile(os.path.expanduser('~/allure.zip')) as z:
    z.extractall(os.path.expanduser('~/'))
print('Extracted!')
"

chmod +x ~/allure-2.27.0/bin/allure
```

**Step 3: Create a wrapper script**

```bash
cat > ~/allure.sh << 'EOF'
#!/bin/bash
export JAVA_HOME="$HOME/jdk-17.0.11+9"
export PATH="$JAVA_HOME/bin:$PATH"
~/allure-2.27.0/bin/allure "$@"
EOF

chmod +x ~/allure.sh
```

**Step 4: Verify**

```bash
~/allure.sh --version
# Expected output: 2.27.0
```

**Step 5: Run tests and serve the report**

```bash
# Run tests first
pytest --alluredir=allure-results

# Serve
~/allure.sh serve allure-results
```

Open the URL printed in the terminal (e.g. `http://localhost:12345/`).

> **Note:** Java and Allure binaries are excluded from the repository via `.gitignore`.
> Each developer must set them up locally following the steps above.
> In GitHub Actions, Allure runs automatically with no manual setup required.

---

### Allure Report Contents

Every test in the Allure report includes:

| Attachment | Description |
|---|---|
| 📸 Screenshot | Full-page browser screenshot taken at test end |
| 🎬 Video | Full screen recording of the entire test execution |

Click any test → scroll to the **Attachments** section to view them inline.

---

## GitHub Actions Setup

The workflow file is located at `.github/workflows/playwright.yml` and triggers automatically on:
- Push to `main` or `master`
- Pull requests targeting `main` or `master`

---

### Live Reports

| Report | URL |
|---|---|
| 🌐 Allure Report (GitHub Pages) | https://robiulislam99.github.io/Books-Automation_Md_Robiul_Islam/allure-report/index.html |
| ⚙️ GitHub Actions Runs | https://github.com/robiulislam99/Books-Automation_Md_Robiul_Islam/actions |

---

### Artifacts uploaded after each run

| Artifact Name | Contents |
|---|---|
| `html-report` | `reports/html/report.html` |
| `allure-results` | Raw Allure JSON results |
| `allure-html-report` | Generated Allure HTML report |
| `screenshots` | Captured screenshots per test |
| `videos` | Recorded videos per test |
| `traces` | Playwright trace files |

To download artifacts: go to your GitHub repository → **Actions** → select a workflow run → scroll to **Artifacts** → click to download.

---

### Viewing the Allure Report online

After every push to `main`, the Allure report is automatically published to GitHub Pages:

```
https://robiulislam99.github.io/Books-Automation_Md_Robiul_Islam/
```

No setup required — just open the link in any browser.

---

## Design Decisions

- **Page Object Model**: Each page has its own class inheriting from `BasePage`. This separates test logic from browser interaction logic, making tests readable and maintainable.
- **Dataclass for BookSummary**: Using `@dataclass` for `BookSummary` gives clear typed contracts between the homepage POM and the test layer.
- **No hardcoded waits**: All synchronisation uses `wait_for_load_state("domcontentloaded")` and Playwright's auto-waiting on locator actions.
- **Randomised selection**: `random.sample()` ensures each run exercises different books, improving overall coverage over time.
- **`requests` for link checks**: Link validation is done at the HTTP layer (not via Playwright navigation) for speed and reliability.

---

## Known Limitations

- **TC-04 (Broken Links)**: Some catalogue pages may return `301` redirects; the `requests` library follows them automatically so they still resolve to 200. If a link redirects to a non-200 page, it will be flagged.
- **TC-02 / TC-03 (Randomisation)**: Tests select from the first page only (20 books). Extending selection across pages would require navigating to collect all books before sampling.
- **Allure CLI**: The Allure CLI must be installed separately; `allure-pytest` only generates the raw results folder.
- **Parallel execution**: The test suite is designed for sequential execution. Parallel runs (e.g., via `pytest-xdist`) would require session-scoped fixtures to be reviewed.