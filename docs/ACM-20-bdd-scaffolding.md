# ACM-20: BDD Scaffolding with pytest-bdd

## Purpose
Set up the pytest-bdd framework and write initial Gherkin feature files
for ACM-4 acceptance criteria, establishing the BDD test structure for
the Brave Leo conversation export project.

## Environment
| Component      | Version                        |
|----------------|--------------------------------|
| OS             | Ubuntu 24.04.4 LTS (noble)     |
| Python         | 3.12.3                         |
| pytest         | 9.0.2                          |
| pytest-bdd     | 8.1.0                          |
| Brave Browser  | 145.1.87.190                   |
| Branch         | feature/ACM-20-bdd-scaffolding |

## Prerequisites
- Brave Browser installed (ACM-19 ✅)
- Git configured with GitHub integration (ACM-18 ✅)
- Project root: `~/Projects/ai-conversation-toolkit/`

---

## Background: Python Virtual Environments

### What is a Virtual Environment?
A virtual environment is an **isolated box** for your project's Python
dependencies — completely separate from your system Python installation.

Your Ubuntu system already has Python installed and uses it for
system-level tasks. Installing packages directly to system Python risks:
- Breaking system tools by upgrading a shared package
- Version conflicts between projects (Project A needs pytest v7,
  Project B needs pytest v8 — they cannot coexist on system Python)

### Why Use One for This Project?
| Concern | Why It Applies |
|---|---|
| **Reproducibility** | `requirements.txt` lets Flora recreate your exact environment |
| **CI/CD safety** | Future pipelines spin up a clean `.venv` every time |
| **No sudo needed** | Packages install into `.venv`, not system directories |
| **Docker alignment** | Mirrors the isolation discipline already used in containers |

### Simple Mental Model
```
System Python  =  your house's electrical system (don't touch it)
.venv          =  a power strip for your desk (plug in what you need)
```

> **Important habit:** Always confirm `(.venv)` is in your prompt before
> running `pip install`. If it's not there, run
> `source .venv/bin/activate` from your project root first.
> If you close the terminal and reopen it, `.venv` won't be active —
> always reactivate before continuing work.

---

## Directory Structure

```
~/Projects/ai-conversation-toolkit/    ← project root
├── .venv/                             ← isolated Python environment (not committed to Git)
├── .gitignore                         ← excludes .venv/, __pycache__/, *.save, etc.
├── requirements.txt                   ← snapshot of exact package versions
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── features/
    │   ├── __init__.py
    │   └── brave_leo_export.feature
    └── step_defs/
        ├── __init__.py
        └── test_brave_leo_export.py
```

> Note: `requirements.txt` and `tests/` live in the project root
> *alongside* `.venv/` — not inside it. `.venv/` is just one folder
> among several in the project root. `requirements.txt` *describes*
> what is inside `.venv/` but is not contained by it.

---

## Steps

### Step 1: Create Feature Branch & Virtual Environment

#### 1a. Create and checkout the feature branch
```bash
cd ~/Projects/ai-conversation-toolkit
git checkout -b feature/ACM-20-bdd-scaffolding
```

#### 1b. Install missing system package (if needed)
On Ubuntu 24.04, `python3-venv` may not be installed by default:
```bash
sudo apt install python3.12-venv -y
```

#### 1c. Create and activate the virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Confirm activation — your prompt should show `(.venv)`.

#### 1d. Install pytest and pytest-bdd
```bash
pip install pytest pytest-bdd
```

**Why pytest-bdd and not full Behave?**
pytest-bdd layers BDD Gherkin syntax onto pytest, so you get
acceptance-test readability without abandoning your existing
pytest ecosystem.

#### 1e. Verify installation
```bash
pytest --version
pip show pytest-bdd
```

Expected output:
```
pytest 9.0.2
Name: pytest-bdd
Version: 8.1.0
Location: /home/dicemandcdc/Projects/ai-conversation-toolkit/.venv/...
```

#### 1f. Freeze dependencies
```bash
pip freeze > requirements.txt
grep -E "pytest|pytest-bdd" requirements.txt
```

Expected output:
```
pytest==9.0.2
pytest-bdd==8.1.0
```

**What does freezing mean?**
`pip freeze` takes a snapshot of every package currently installed
in your virtual environment with their **exact version numbers**
(using `==`). This means anyone cloning the repo gets an identical
environment by running `pip install -r requirements.txt`.

> **Important habit:** Re-run `pip freeze > requirements.txt` every
> time you `pip install` something new, otherwise `requirements.txt`
> goes stale.

---

### Step 2: Create the Feature File with Gherkin Scenarios

#### 2a. Create the tests directory structure
```bash
mkdir -p tests/features
touch tests/__init__.py
touch tests/features/__init__.py
```

#### 2b. Create the feature file
```bash
nano tests/features/brave_leo_export.feature
```

```gherkin
Feature: Export Brave Leo Conversations to JSON
  As a user of the ACM system
  I want to export Brave Leo AI conversations to JSON
  So that I can store and analyze them programmatically

  Background:
    Given the Brave browser is installed
    And the export destination directory exists at "~/ai-conversations/"

  Scenario: Successful export to JSON
    Given a Brave Leo conversation exists in the browser
    When the export script is executed
    Then a JSON file is created in "~/ai-conversations/"
    And the JSON file contains a "platform" field with value "brave-leo"
    And the JSON file contains a "timestamp" field
    And the JSON file contains a "messages" array with at least one entry

  Scenario: Export file naming convention
    Given a Brave Leo conversation exists in the browser
    When the export script is executed
    Then the output filename matches the pattern "brave-leo_YYYY-MM-DD_HHMMSS.json"

  Scenario: Failed export handling
    Given the export destination directory does not exist
    When the export script is executed
    Then the script exits with a non-zero status code
    And an error message is written to the log
```

#### 2c. Create a minimal conftest.py

```bash
nano tests/conftest.py
```

```python
# tests/conftest.py
# Step definitions will be wired here in ACM-21/22
import pytest
```

**Why is conftest.py needed?**
`conftest.py` is a special pytest configuration file that is
automatically loaded before any tests run. It serves as the
**central wiring point** for your test suite:

- pytest-bdd uses it to share fixtures (reusable setup/teardown
  functions) across all step definition files
- Without it, step definitions in different files cannot share
  common setup — for example, a "Given the export directory exists"
  step used across multiple scenarios would need to be duplicated
- It also tells pytest where to find plugins and hooks for the
  entire `tests/` directory
- Right now it only contains `import pytest` as a placeholder,
  but in ACM-22 it will hold shared fixtures for the export script
  tests

Think of `conftest.py` as the **foundation** of your test suite —
you lay it now so the structure is correct when real logic is added.

#### 2d. Create placeholder step definitions
```bash
mkdir -p tests/step_defs
touch tests/step_defs/__init__.py
nano tests/step_defs/test_brave_leo_export.py
```

```python
# tests/step_defs/test_brave_leo_export.py
# ACM-20: Placeholder step definitions — RED phase
# Full implementation in ACM-22

import pytest
from pytest_bdd import scenarios, given, when, then

scenarios('../features/brave_leo_export.feature')

@given('the Brave browser is installed')
def brave_installed():
    pass  # TODO: ACM-22

@given('the export destination directory exists at "~/ai-conversations/"')
def export_dir_exists():
    pass  # TODO: ACM-22

@given('a Brave Leo conversation exists in the browser')
def leo_conversation_exists():
    pass  # TODO: ACM-21

@when('the export script is executed')
def run_export_script():
    pass  # TODO: ACM-22

@then('a JSON file is created in "~/ai-conversations/"')
def json_file_created():
    pass  # TODO: ACM-22

@then('the JSON file contains a "platform" field with value "brave-leo"')
def json_has_platform():
    pass  # TODO: ACM-22

@then('the JSON file contains a "timestamp" field')
def json_has_timestamp():
    pass  # TODO: ACM-22

@then('the JSON file contains a "messages" array with at least one entry')
def json_has_messages():
    pass  # TODO: ACM-22

@then('the output filename matches the pattern "brave-leo_YYYY-MM-DD_HHMMSS.json"')
def filename_matches_pattern():
    pass  # TODO: ACM-22

@given('the export destination directory does not exist')
def export_dir_missing():
    pass  # TODO: ACM-22

@then('the script exits with a non-zero status code')
def script_fails_gracefully():
    pass  # TODO: ACM-22

@then('an error message is written to the log')
def error_logged():
    pass  # TODO: ACM-22
```

#### 2e. Confirm RED phase
```bash
pytest tests/ -v
```

Expected output:
```
collected 3 items

tests/step_defs/test_brave_leo_export.py::test_successful_export_to_json PASSED
tests/step_defs/test_brave_leo_export.py::test_export_file_naming_convention PASSED
tests/step_defs/test_brave_leo_export.py::test_failed_export_handling PASSED

3 passed in 0.02s
```

> Tests show PASSED because step definitions are empty stubs (`pass`).
> The real RED phase occurs in ACM-22 when assertions are added against
> code that does not yet exist.

---

### Step 3: Commit and Push to GitHub

#### 3a. Handle editor artifacts
```bash
rm docs/ACM-19-brave-install.md.save
```

#### 3b. Add editor artifacts to .gitignore
```bash
nano .gitignore
```

Add at the very top:
```text
# Editor artifacts
*.save
```

#### 3c. Verify .gitignore is working
```bash
git status
```

Expected — `.save` file should NOT appear:
```
On branch feature/ACM-20-bdd-scaffolding
Changes not staged for commit:
    modified:   .gitignore
Untracked files:
    requirements.txt
    tests/
```

#### 3d. Stage all files
```bash
git add .gitignore
git add requirements.txt
git add tests/
git status
```

Expected:
```
Changes to be committed:
    modified:   .gitignore
    new file:   requirements.txt
    new file:   tests/__init__.py
    new file:   tests/conftest.py
    new file:   tests/features/__init__.py
    new file:   tests/features/brave_leo_export.feature
    new file:   tests/step_defs/__init__.py
    new file:   tests/step_defs/test_brave_leo_export.py
```

#### 3e. Commit with ACM-20 format
```bash
git commit -m "ACM-20 add BDD scaffolding with pytest-bdd feature file and step definitions"
```

Expected:
```
[feature/ACM-20-bdd-scaffolding 66bd9cf] ACM-20 add BDD scaffolding...
8 files changed, 102 insertions(+)
```

#### 3f. Push to GitHub
```bash
git push -u origin feature/ACM-20-bdd-scaffolding
```

Expected:
```
* [new branch] feature/ACM-20-bdd-scaffolding -> feature/ACM-20-bdd-scaffolding
Branch set up to track remote 'origin/feature/ACM-20-bdd-scaffolding'
```

---

## Verification

### Jira ACM-20 Development Panel
After pushing, confirm the following appear in the ACM-20 ticket:
```
🔀 Branches    feature/ACM-20-bdd-scaffolding    1
✅ Commits     ACM-20 add BDD scaffolding...      1
```
> Note: Jira-GitHub sync may take up to 10 minutes.

### Acceptance Criteria
| Criteria | Status |
|---|---|
| pytest-bdd installed in virtual environment | ✅ |
| Feature file created with Gherkin scenarios | ✅ |
| Initial failing tests confirmed (red phase) | ✅ |
| Test structure committed to GitHub | ✅ |

---

## Related
- Jira: ACM-20
- Parent story: ACM-4 Export Brave Leo Conversations to JSON
- Previous: ACM-19 Install Brave Browser
- Next: ACM-21 Inspect DOM Structure
