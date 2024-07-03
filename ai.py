from openai import OpenAI
from config import Config

client = OpenAI(
    api_key=Config.OPENAI_API_KEY,
)

def judge_idea(idea):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in evaluating hackathon ideas."},
            {"role": "user", "content": f"Evaluate the following hackathon idea and provide a score out of 10 with a brief explanation:\n\nIdea: {idea}"}
        ]
    )
    return response.choices[0].message.content

def time_managmet(idea):
    pass
