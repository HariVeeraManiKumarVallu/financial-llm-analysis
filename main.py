from src.ingestion import load_financial_data
from src.preprocessing import clean_data
from src.embedding import dataframe_to_text, create_embeddings
from src.prompt_engineering import load_prompt_template, build_prompt
from src.llm_pipeline import generate_summary

RAW_DATA_PATH = "data/raw/financial_data.csv"


def run_pipeline():

    df = load_financial_data(RAW_DATA_PATH)

    df = clean_data(df)

    texts = dataframe_to_text(df)

    embeddings = create_embeddings(texts)

    context = "\n".join(texts)

    template = load_prompt_template("prompts/financial_prompt.txt")

    prompt = build_prompt(template, context)

    result = generate_summary(prompt)

    print("\nFinancial Insights:\n")
    print(result)


if __name__ == "__main__":
    run_pipeline()