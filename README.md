# TDS Virtual TA

This repository contains:

- A **scraper** (`scraper/discourse_scraper.py`) that pulls TDS January–April 2025 Discourse posts.
- A **FastAPI** server (`api/main.py`) exposing a `/api/` endpoint to answer student questions.
- A **Promptfoo** test suite (`promptfoo.config.yaml`) for automated evaluation.
- Deployment-ready setup for Heroku (via `Procfile`) or other hosts.

## Setup

```bash
# 1. Clone & enter
git clone git@github.com:23f2000673/tds-virtual-ta.git
cd tds-virtual-ta

# 2. Create & activate Python venv
python3 -m venv venv
source venv/bin/activate

# 3. Install deps
pip install -r requirements.txt
npm install

# 4. (Tomorrow) export your Discourse cookies:
#    export DISCOURSE_SESSION_COOKIE="…"
#    export DISCOURSE_T_COOKIE="…"

# 5. Scrape data
python3 scraper/discourse_scraper.py

# 6. Run API locally
uvicorn api.main:app --reload

# 7. Test with Promptfoo
npm test
```
