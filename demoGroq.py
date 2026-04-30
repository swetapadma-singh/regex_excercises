# from groq import Groq

# client = Groq()

# response = client.chat.completions.create(
#     model="llama-3.3-70b-versatile",
#     messages=[
#       {
#         "role": "user",
#         "content": "What is capital of France ? explain in one line"
#       }
#     ]
# )

# print(response.choices[0].message.content)








import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras()

completion = client.chat.completions.create(
    messages=[{"role":"user","content":"multiplication table of 12 ?"}],
    model="llama3.1-8b",
    max_completion_tokens=1024,
    temperature=0.2,
    top_p=1,
    stream=False
)

print(completion.choices[0].message.content)