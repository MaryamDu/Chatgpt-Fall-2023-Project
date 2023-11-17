import openai
import json


file = open("fantasy-solution.pddl")

content = file.readlines()
# countFile = content.split("\n")

prompt = ""

count = 0

# .length of the file (total number of the lines)
for i in content:
    if i:
        count += 1

lines = []

# make an array for 2 - .length-1
i = 2
while i != count:
    lines.append(i)
    i += 1

for pos, lineNum in enumerate(content):
    if pos in lines:
        prompt = lineNum
        #print(prompt) 

file.close()

postprompt = "Write a chapter based story from the first chapter to chapter number " + str(count) + "based on the following steps where each line is a new chapter that only lasts a few paragraphs: " + prompt


completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo",
  temperature = 0.8, #degree of randomness between 0 and 2
  max_tokens = 2000,
  messages = [
    {"role": "system", "content": "You are a story teller."},
    {"role": "user", "content": postprompt},
    {"role": "assistant", "content": "Rory confesses exuberantly, \"I want to spend the rest of my life with you! Let's go on an adventure together!\""},
  ]
)

output = open("story.txt", "w")
stroutput = str(completion["choices"][0].message["content"])
output.write(stroutput)
output.close()

print(completion["choices"][0].message["content"])
# print(completion["choices"][0].message["content"], file=output)
# print(completion.choices[0].message)
