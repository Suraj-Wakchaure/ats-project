from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


def get_summary(candidate_name, skills, score, job_title, required_skills):
    api_key = os.getenv('API_KEY')
    client = Groq(api_key=api_key)
    
    response = client.chat.completions.create(
        model='llama-3.1-8b-instant',
        messages=[{
            "role": "user",
            "content": f"""In one sentence summarize this candidate for {job_title}:
            Name: {candidate_name}
            Candidate skills: {skills}
            Required skills: {required_skills}
            Match score: {score}%
            Be concise and professional."""
        }],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()
