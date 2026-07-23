from google import genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Function to ask Gemini
def ask_gemini(title, prompt):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print("Prompt:")
    print(prompt)
    print("\nResponse:\n")

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    print(response.text)


# Zero-shot Prompting
zero_prompt = "Explain Machine Learning in simple words."

# One-shot Prompting
one_prompt = """
Example:
Apple -> Fruit

Now answer:
Carrot ->
"""

# Few-shot Prompting
few_prompt = """
Apple -> Fruit
Carrot -> Vegetable
Tiger -> Animal

Rose ->
"""

# Chain-of-Thought Prompting
cot_prompt = """
A notebook costs ₹40.
Rahul buys 5 notebooks.

Think step by step and calculate the total amount.
"""

ask_gemini("ZERO-SHOT PROMPTING", zero_prompt)
ask_gemini("ONE-SHOT PROMPTING", one_prompt)
ask_gemini("FEW-SHOT PROMPTING", few_prompt)
ask_gemini("CHAIN-OF-THOUGHT PROMPTING", cot_prompt)