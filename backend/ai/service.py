import json
import openai  # Or local LLM

def recommend_charts(schema):
    prompt = f"You are an AI data analyst. Given {schema}, recommend charts as JSON array."
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    return json.loads(response.choices[0].message.content)