import os
import openai
import time
#print time in HH:MM:SS format
print("Current Time =", time.strftime("%H:%M:%S", time.localtime()))
openai.api_key = "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"
#####################################################################
# response = openai.Image.create(
#   prompt="a lotus logo",
#   n=1,
#   size="1024x1024"
# )
# image_url = response['data'][0]['url']
# print(image_url)
#####################################################################
response = openai.Completion.create(
  model="text-davinci-003",
  prompt="How are you doing today?",
  temperature=0.5,
  max_tokens=1000,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0,
)
# print(response['choices'][0]['text'])
print(response)

#####################################################################
print("Current Time =", time.strftime("%H:%M:%S", time.localtime()))
print("done")