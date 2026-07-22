# Sugar News

Sugar News is an independent project for generating and publishing the daily global sugar-industry news dashboard.

## Project Layout

```text
sugar-news/
├── .github/workflows/sugar-news.yml
├── AGENTS.md
├── README.md
├── prompts/
│   └── sugar_news_prompt.md
├── public/
│   └── sugar-news/
│       ├── index.html
│       ├── data/
│       ├── templates/
│       └── vendor/
├── data/
│   └── verified_news/YYYY/MM/sugar_news_YYYY-MM-DD.json
├── logs/
├── reports/
├── scripts/
└── templates/
```

## Local Run

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Generate a target date:

```powershell
python scripts/sugar_news_pipeline.py --date 2026-07-21 --offline-only
```

Verify local dashboard data:

```powershell
python scripts/verify_sugar_news_dashboard.py --date 2026-07-21
```

Serve locally from the project root:

```powershell
python -m http.server 8765
```

Then open:

```text
http://127.0.0.1:8765/public/sugar-news/index.html
```

## Deployment

Create a dedicated GitHub repository and connect it to a dedicated Vercel project. The Vercel project should serve this repository root and use:

- Build Command: none
- Output Directory: none
- Framework Preset: Other / Static
- Node.js Version: 24.x or the Vercel account default
- Production route: `/`

The included `vercel.json` maps `/` to the Sugar News dashboard and keeps `/sugar-news` as a same-project compatibility route.

## Automation

The GitHub Actions workflow runs at:

```text
0 22 * * *   # Beijing 06:00 next day
10 22 * * *  # Beijing 06:10 retry
30 22 * * *  # Beijing 06:30 retry
```

Repository configuration:

- Variables: `SUGAR_NEWS_BASE_URL`, `OPENAI_MODEL`
- Secrets: `OPENAI_API_KEY`, `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`

Do not commit secret values. Store them only in GitHub Actions secrets and Vercel environment variables.

## Environment Names

Runtime and automation may use these names:

- `TZ`
- `PYTHONIOENCODING`
- `SUGAR_NEWS_ROOT`
- `SUGAR_NEWS_NOW`
- `SUGAR_NEWS_METRIC_REFRESH_TIMEOUT`
- `SUGAR_NEWS_BASE_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

## Data Rules

- `data/verified_news` is the source of truth for audited news.
- `reports` stores generated Excel files.
- `public/sugar-news/data` stores dashboard JSON consumed by the browser.
- Brazil and India metric histories live under `public/sugar-news/data/brazil_metrics` and `public/sugar-news/data/india_metrics`.
- Generated dashboard data must never read or write another project directory.
