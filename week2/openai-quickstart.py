import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-4o",
    instructions="You are a helpful teacher who explains technical concepts simply.",
    input="Explain what an API is in one simple sentence.",
)

print(response.output_text)
# Style 1:
# developer instructions + user input

# Style 2:
# instructions + input