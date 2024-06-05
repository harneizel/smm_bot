from openai import OpenAI
client = OpenAI(api_key='sk-proj-9wv8fr0fpt9O7jBTl8iaT3BlbkFJVgZdHBp6x3tT9KOrNkgE')

response = client.chat.completions.create(
  model="gpt-4o",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "Как твои дела?."}
  ]
)
print(response.choices[0].message.content)