from google import genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

print("=" * 50)
print("      🤖 AI Chatbot using Gemini")
print("Type 'exit' to quit")
print("=" * 50)

while True:
    question = input("\nYou: ")

    if question.lower() == "exit":
        print("\nBot: Goodbye! Have a nice day. 😊")
        break

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=question
        )

        print("\nBot:", response.text)

    except Exception as e:
        print("\nError:", e)