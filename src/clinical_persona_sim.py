"""Main simulation engine for LLM-based clinical persona responses.

Runs each synthetic persona through all clinical assessment batteries using
Google Gemini, collecting structured JSON responses and writing results to CSV.
"""

import argparse
import csv
import json
import os
import random
import time

import google.generativeai as genai
from dotenv import load_dotenv

from personas import personas
from batteries import batteries

# Constants
MODEL_NAME = "gemini-2.0-flash"
OUTPUT_FILE = "../data/simulation_results.csv"

# Load environment variables
load_dotenv()

# Configure API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("WARNING: GOOGLE_API_KEY not found. Please set it in a .env file.")
else:
    genai.configure(api_key=api_key)


class SyntheticRespondent:
    """An LLM-backed agent that answers clinical questionnaires in character.

    Maintains conversation history across batteries to ensure response
    consistency within a single persona.
    """

    def __init__(self, profile, model_name=MODEL_NAME):
        self.profile = profile
        self.history = []
        self.model = genai.GenerativeModel(model_name)

    def _get_system_prompt(self, current_questions):
        profile_json = json.dumps(self.profile, indent=2)
        history_json = json.dumps(self.history, indent=2)
        questions_json = json.dumps(current_questions, indent=2)

        prompt = f"""
        Your task is to answer questions. The questions, their types, and possible answers are below (JSON).
        
        Answer consistently pretending you are a person with the following profile:
        {profile_json}
        
        You must remain consistent with prior answers. Here they are:
        {history_json}
        
        Here are the new question(s) to answer (JSON):
        {questions_json}
        
        You must answer each question. Some questions will include context and instructions on how to respond.
        
        CRITICAL INSTRUCTIONS:
        1. You do not have an encyclopedic memory. Your knowledge should correspond to your education and background.
        2. If someone with the assigned profile would realistically not know an answer, respond with 'I don't know' or similar.
        3. Do not invent knowledge you wouldn't have.
        4. Write in a style consistent with your profile (e.g., if education is low, grammar/spelling should reflect that).
        5. Never write more than 20 words for text responses.
        
        Return results in the following JSON structure:
        {{
            "responses": [
                {{
                    "question_id": "...",
                    "answer_type": "...",
                    "value": "..." 
                }}
            ]
        }}
        """
        return prompt

    def answer_survey(self, questions):
        """Send a battery's questions to the LLM and return parsed JSON responses."""
        prompt = self._get_system_prompt(questions)
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            response_data = json.loads(response.text)
            
            for resp in response_data.get('responses', []):
                orig_q = next((q for q in questions if q['question_id'] == resp['question_id']), None)
                if orig_q:
                    self.history.append({
                        "question_id": resp['question_id'],
                        "question_text": orig_q['question_text'],
                        "answer_value": resp['value']
                    })
            return response_data
        except Exception as e:
            print(f"Error generating response: {e}")
            return None

def run_full_simulation():
    """Run all personas through all batteries, writing results to CSV."""
    parser = argparse.ArgumentParser(description='Run Clinical Persona Simulation')
    parser.add_argument('--mock', action='store_true', help='Run in mock mode without API calls')
    args = parser.parse_args()

    results_file = OUTPUT_FILE
    
    # Initialize CSV
    with open(results_file, 'w', newline='') as csvfile:
        fieldnames = ['Persona_ID', 'Diagnosis', 'Severity', 'Battery', 'Question_ID', 'Question_Text', 'Response_Value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for persona in personas:
            print(f"\n--- Simulating Persona: {persona['id']} ({persona['clinical_profile']['diagnosis']} - {persona['clinical_profile']['severity']}) ---")
            
            bot = SyntheticRespondent(persona)
            
            for battery_name, questions in batteries.items():
                print(f"  Running Battery: {battery_name}...")
                
                if args.mock:
                    # Mock response generation
                    print("    [MOCK] Generating random responses...")
                    responses = {"responses": []}
                    for q in questions:
                        if q["question_type"] == "text" or not q["question_response_options"]:
                            val = "5" # Mock text response
                        else:
                            val = random.choice(q["question_response_options"])
                        
                        responses["responses"].append({
                            "question_id": q["question_id"],
                            "answer_type": q["question_type"],
                            "value": val
                        })
                    time.sleep(0.1) # Fast mock
                else:
                    responses = bot.answer_survey(questions)
                    time.sleep(1)
                
                if responses:
                    for resp in responses.get('responses', []):
                        # Find original question text
                        orig_q = next((q for q in questions if q['question_id'] == resp['question_id']), None)
                        
                        writer.writerow({
                            'Persona_ID': persona['id'],
                            'Diagnosis': persona['clinical_profile']['diagnosis'],
                            'Severity': persona['clinical_profile']['severity'],
                            'Battery': battery_name,
                            'Question_ID': resp['question_id'],
                            'Question_Text': orig_q['question_text'] if orig_q else "Unknown",
                            'Response_Value': resp['value']
                        })
                        # Flush to ensure data is saved incrementally
                        csvfile.flush()
                else:
                    print(f"    Failed to get responses for {battery_name}")

    print(f"\nSimulation complete. Results saved to {results_file}")

if __name__ == "__main__":
    run_full_simulation()
