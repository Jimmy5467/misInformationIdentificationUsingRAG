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