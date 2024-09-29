import openai

def check_openai_api_key(api_key):
    client = openai.OpenAI(api_key=api_key)
    try:
        client.models.list()
    except openai.AuthenticationError:
        return False
    else:
        return True


OPENAI_API_KEY = "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"

if check_openai_api_key(OPENAI_API_KEY):
    print("Valid OpenAI API key.")
else:
    print("Invalid OpenAI API key.")