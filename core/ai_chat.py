import anthropic, os

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def ask_ai(question):
    res = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=600,
        messages=[{"role": "user", "content": question}]
    )
    return res.content[0].text
