import requests
import google.generativeai as genai

# Whisper API configuration
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
headers = {"Authorization": "Bearer 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"}

# Gemini API configuration
GOOGLE_API_KEY = "AIzaSyAmmJdR44ByOvMT9oUnH3e2GGbSXaxpUEw"
genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = "models/gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def analyze_transcript(transcript):
    prompt = f"""You are an AI assistant tasked with analyzing and grading a transcript of an interview. The transcript follows a conversational format, with roles clearly indicated as Interviewer and Candidate. Your job is to evaluate the Candidate’s responses, assign a grade, and provide constructive feedback.

Transcript Format:
The transcript will appear as follows:
Interviewer: [Question or statement]
Candidate: [Response]

Your Task:
Identify Roles: Ensure that you differentiate between the Interviewer's and the Candidate's parts.
Evaluate Responses:
Carefully assess how the Candidate answers the Interviewer's questions.
Check for relevance, accuracy, depth, clarity, and logical reasoning in the Candidate’s responses.
Determine whether the Candidate addressed all aspects of each question effectively.
Grading Format:
Assign a grade on a scale of 1 to 10:
10: Outstanding responses (highly relevant, accurate, and well-articulated).
5: Average responses (partially relevant or lacking in depth).
1: Poor responses (irrelevant, incorrect, or unclear).
Justification and Feedback:
Provide a justification for the grade, highlighting strengths and weaknesses.
Offer constructive suggestions for improving the Candidate’s performance in future interviews.
Example Analysis:
For each question and response, format your evaluation as follows:

Interviewer: [Insert Interviewer’s Question]
Candidate: [Insert Candidate’s Answer]

Evaluation: 
- Strengths: [List any positives in the Candidate’s response]
- Weaknesses: [List areas where the Candidate’s response fell short]
Grade for this Question: [Score out of 10]

Final Report:
At the end of the analysis:

Provide an overall grade for the Candidate.
Summarize key strengths and weaknesses.
Offer general suggestions for improvement.

Transcript: {transcript}"""
    response = model.generate_content(prompt)
    return response.text

# Generate transcript
output = query("audio.mp3")
transcript = output["text"]

# Analyze transcript using Gemini
analysis = analyze_transcript(transcript)

# Save transcript and analysis separately
with open("transcript.md", "w", encoding="utf-8") as f:
    f.write("# Original Transcript\n\n")
    f.write(transcript)

with open("analysis.md", "w", encoding="utf-8") as f:
    f.write("# Interview Analysis\n\n")
    f.write(analysis)