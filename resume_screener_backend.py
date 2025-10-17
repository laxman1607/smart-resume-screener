import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- FLASK SETUP ---
# Initialize Flask application
app = Flask(__name__)
# Enable CORS for the frontend running in the Canvas (or locally)
CORS(app)

# --- GEMINI API KEY SETUP ---
# Fetch the API key from environment variables
try:
    API_KEY = os.environ['GEMINI_API_KEY']
except KeyError:
    # If the key is not set, log an error and exit gracefully
    print("FATAL ERROR: GEMINI_API_KEY environment variable not set.")
    print("Please set the environment variable and restart the application.")
    exit(1)

# Initialize the Gemini Client
# Note: If this line throws an error, it means the API key is invalid or permissions are wrong.
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"FATAL ERROR: Could not initialize Gemini client. Check API key validity. Error: {e}")
    exit(1)


# --- LLM CONFIGURATION ---
MODEL_NAME = 'gemini-2.5-flash'

# System instruction to guide the model's behavior and output format
SYSTEM_INSTRUCTION = """
You are a highly efficient and accurate Senior Technical Recruiter AI.
Your task is to analyze a candidate's resume against a Job Description (JD).
You must follow these steps precisely:
1. Score the candidate's match level on a scale of 1 to 10 (1 being a poor match, 10 being a perfect match).
2. Identify the top 3-5 technical and experience-related Strengths that align directly with the JD.
3. Identify 1-3 critical Gaps (missing required skills, insufficient experience, etc.) relative to the JD. If no gaps are found, return "None identified."

Your entire response MUST be a single, valid JSON object that strictly adheres to the provided JSON schema.
Ensure the 'candidate_name' is extracted from the resume if possible, otherwise use a generic label like 'Candidate 1'.
"""

# FIX: Explicitly adding 'OPTIONS' to the methods list to resolve the 404 pre-flight error.
@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_candidates_route():
    """
    Handles POST requests for candidate analysis.
    Receives JD and a list of candidates, sends each to the Gemini API for scoring.
    """
    if request.method == 'OPTIONS':
        # The CORS library should handle this, but adding a safe handler just in case
        return jsonify({'status': 'ok'}), 200

    try:
        data = request.json
        job_description = data.get('job_description')
        candidates = data.get('candidates', [])

        if not job_description or not candidates:
            return jsonify({"status": "error", "message": "Missing job_description or candidates data."}), 400

        results = []
        
        # Define the strict JSON schema for the model's response
        response_schema = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "match_score": types.Schema(type=types.Type.INTEGER, description="The candidate's score on a scale of 1-10."),
                "candidate_name": types.Schema(type=types.Type.STRING, description="The name of the candidate, extracted from the resume."),
                "key_strengths": types.Schema(type=types.Type.STRING, description="A single paragraph listing 3-5 key strengths relevant to the JD."),
                "identified_gaps": types.Schema(type=types.Type.STRING, description="A single paragraph listing 1-3 critical gaps. Use 'None identified.' if none are found."),
            },
            required=["match_score", "candidate_name", "key_strengths", "identified_gaps"]
        )

        # Iterate through each candidate for analysis
        for candidate in candidates:
            candidate_id = candidate.get('id', 'Unknown Candidate')
            resume_text = candidate.get('resume_text')

            if not resume_text:
                results.append({
                    "candidate_id": candidate_id,
                    "analysis": {"candidate_name": candidate_id, "match_score": 0, "key_strengths": "No resume text provided.", "identified_gaps": "No resume text provided."}
                })
                continue

            # Construct the user prompt
            user_prompt = f"Job Description:\n---\n{job_description}\n---\nCandidate Resume:\n---\n{resume_text}\n---\nAnalyze this resume against the JD and return the results as a single JSON object."

            # Exponential Backoff (Client SDK handles retries, so we just handle API errors here)
            try:
                # Call the Gemini API for structured generation
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=[user_prompt],
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        response_mime_type="application/json",
                        response_schema=response_schema,
                    )
                )

                # The response text will be the JSON string
                analysis_json = response.text
                analysis_data = json.loads(analysis_json)
                
                results.append({
                    "candidate_id": candidate_id,
                    "analysis": analysis_data
                })

            except APIError as e:
                # Log the API error for debugging in the terminal
                app.logger.error(f"Gemini API Error for {candidate_id}: {e}")
                results.append({
                    "candidate_id": candidate_id,
                    "analysis": {"candidate_name": candidate_id, "match_score": None, "key_strengths": f"API Error: {str(e)}", "identified_gaps": "Check backend terminal for details."}
                })
            except json.JSONDecodeError:
                # Log invalid JSON response
                app.logger.error(f"JSON Decode Error for {candidate_id}. Raw response: {response.text[:100]}...")
                results.append({
                    "candidate_id": candidate_id,
                    "analysis": {"candidate_name": candidate_id, "match_score": None, "key_strengths": "LLM returned invalid JSON.", "identified_gaps": "Check backend terminal for details."}
                })
            except Exception as e:
                # Log any other unexpected errors
                app.logger.error(f"Unexpected Error for {candidate_id}: {e}")
                results.append({
                    "candidate_id": candidate_id,
                    "analysis": {"candidate_name": candidate_id, "match_score": None, "key_strengths": f"Unexpected Error: {str(e)}", "identified_gaps": "Check backend terminal for details."}
                })

        return jsonify({"status": "success", "results": results})

    except Exception as e:
        app.logger.error(f"Internal Server Error: {e}")
        return jsonify({"status": "error", "message": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Running on port 8080 to match the frontend and avoid common firewall issues on 5000
    app.run(debug=True, port=8080)
