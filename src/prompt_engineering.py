def load_prompt_template(path):
    with open(path, "r") as f:
        return f.read()


def build_prompt(template, context):
    """
    Inject retrieved financial data into prompt template.
    """
    return template.replace("{context}", context)