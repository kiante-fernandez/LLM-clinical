"""List available Google Generative AI models that support content generation."""

import google.generativeai as genai
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")


if __name__ == "__main__":
    main()
