import anthropic, os

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

MODEL = "claude-3-5-sonnet-latest"

def ask_ai(question):
    res = client.messages.create(
        model=MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content": question}]
    )
    return res.content[0].text
