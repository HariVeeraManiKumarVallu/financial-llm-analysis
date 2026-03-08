from fastapi import FastAPI, HTTPException
from src.ingestion import load_financial_data
from src.preprocessing import clean_data
from src.embedding import dataframe_to_text, create_embeddings
from src.prompt_engineering import load_prompt_template, build_prompt
from src.llm_pipeline import generate_summary

app = FastAPI()

@app.get("/financial-insights")

def get_insights():

    df = load_financial_data("data/raw/financial_data.csv")
    df = clean_data(df)

    texts = dataframe_to_text(df)
    embeddings = create_embeddings(texts)

    context = "\n".join(texts)

    template = load_prompt_template("prompts/financial_prompt.txt")
    prompt = build_prompt(template, context)

    try:
        summary = generate_summary(prompt)
    except RuntimeError as exc:
        message = str(exc)
        if "HTTP 503" in message or "UNAVAILABLE" in message:
            raise HTTPException(status_code=503, detail=message) from exc
        raise HTTPException(status_code=500, detail=message) from exc

    return {"analysis": summary}
