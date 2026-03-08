# Financial LLM Analysis

Financial data analysis pipeline using:
- `sentence-transformers` for embeddings
- Prompt templating for context construction
- Google Gemini (`gemini-flash-latest`) for generated financial insights
- FastAPI for API access

## Project Structure

```text
financial-llm-analysis/
|- app/
|  |- api_server.py
|- config/
|  |- config.yaml
|- data/
|  |- raw/financial_data.csv
|  |- processed/cleaned_financial_data.csv
|- prompts/
|  |- financial_prompt.txt
|- src/
|  |- embedding.py
|  |- ingestion.py
|  |- llm_pipeline.py
|  |- preprocessing.py
|  |- prompt_engineering.py
|  |- retriever.py
|- main.py
|- requirements.txt
```

## Prerequisites

- Python 3.10+ (tested with 3.13)
- A valid Gemini API key

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Set your Gemini key (PowerShell session only):

```powershell
$env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Persist across new terminals:

```powershell
setx GEMINI_API_KEY "YOUR_GEMINI_API_KEY"
```

## Run Pipeline (CLI)

```powershell
python .\main.py
```

This prints generated financial insights to the terminal.

## Run API Server

```powershell
python -m uvicorn app.api_server:app --reload
```

Useful URLs:
- API docs: `http://127.0.0.1:8000/docs`
- Endpoint: `GET http://127.0.0.1:8000/financial-insights`

## Configuration

Configuration file: `config/config.yaml`

Current LLM settings:
- `llm_provider: gemini`
- `llm_model: gemini-flash-latest`

## Error Notes

- `HTTP 503 UNAVAILABLE` from Gemini means temporary high demand. The code retries automatically.
- Hugging Face unauthenticated warning is informational and usually safe to ignore.

## CI/CD (GitHub Actions)

Workflows are defined in:
- `.github/workflows/ci.yml` (basic Python compile validation)
- `.github/workflows/cd.yml` (packages and uploads a build artifact)

They run on pushes to `main`/`master` and on manual trigger.

## Security

- Do not commit API keys to source control.
- Rotate any key that was shared publicly.
