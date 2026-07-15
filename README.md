# Locobuzz Regression Suites

Selenium / Playwright regression + smoke suites for the Locobuzz CX platform
(staging + pre-prod). This repo contains **only** the test suites and their
support code — no application/product code.

## Layout

| Folder | What's in it |
|---|---|
| `Suites/` | Channel suites (Twitter, Facebook, Instagram, LinkedIn, YouTube, Email) and suite runners |
| `tests/` | Selenium + Playwright test cases, organized by module |
| `PreProd Regression/` | Pre-prod regression entrypoint |
| `elements/` | Page objects / element locators |
| `helpers/` | Report generation + email report helpers |
| `locobuzz_login/` | Login flows (CX / UAT / PreProd) |
| `config/` | Ticket IDs and shared config |
| `utils/` | Credential + PDF helpers |

## Setup

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

pip install -r requirements.txt

# Copy the env template and fill in credentials locally (never commit .env)
cp .env.example .env
```

## Running

```bash
# All suites
python Suites/run_all_suites.py

# A single channel suite
pytest Suites/test_twitter_suite.py

# Pre-prod regression
python "PreProd Regression/preprod_reg.py/preprod_reg.py"
```

Credentials are read from environment variables / `.env` — see `.env.example`.
Nothing sensitive is committed to this repo.
